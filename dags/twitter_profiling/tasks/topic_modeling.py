import torch
import umap
import pandas as pd
from sklearn.cluster import DBSCAN
import numpy as np
from transformers import AutoModel, AutoTokenizer
import yake
from twitter_profiling.db.db_session import session
from twitter_profiling.model.tweet import Tweet
from twitter_profiling.model.user import User
import matplotlib.pyplot as plt
from twitter_profiling.util import create_static_folder
from twitter_profiling.model.topic_modeling import TopicModeling
from twitter_profiling import STATIC_FOLDER
from sklearn.feature_extraction.text import TfidfVectorizer
from kneed import KneeLocator
import demoji
import re
from sklearn.neighbors import NearestNeighbors



def plot_clusters(labels, n_clusters_, db, umap_embeddings, exec_id):
    unique_labels = set(labels)
    core_samples_mask = np.zeros_like(labels, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True

    colors = [plt.cm.Spectral(each) for each in np.linspace(0, 1, len(unique_labels))]
    for k, col in zip(unique_labels, colors):
        if k == -1:
            # Black used for noise.
            col = [0, 0, 0, 1]

        class_member_mask = labels == k

        xy = umap_embeddings[class_member_mask & core_samples_mask]
        plt.plot(
            xy[:, 0],
            xy[:, 1],
            "o",
            markerfacecolor=tuple(col),
            markeredgecolor="k",
            markersize=14,
        )

        xy = umap_embeddings[class_member_mask & ~core_samples_mask]
        plt.plot(
            xy[:, 0],
            xy[:, 1],
            "o",
            markerfacecolor=tuple(col),
            markeredgecolor="k",
            markersize=6,
        )
    plt.title(f"Estimated number of clusters: {n_clusters_}")
    create_static_folder(exec_id)
    plt.savefig(STATIC_FOLDER+exec_id+"/clusters")


def clean_tweet(tweet):
    tweet = re.sub(r'@\w*', '', tweet).lower()
    tweet = demoji.replace(tweet, "")
    return re.sub(r'https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&\/=]*)', '', tweet)


def get_topics(df):
    topics = []
    kw = []
    clusters = list(df["cluster"].unique())
    for cluster in clusters:
        topics.append((cluster, " ".join(list(df[df['cluster'] == cluster]['text']))))
    kw_extractor = yake.KeywordExtractor(n=1, top=5)
    for cluster, topic in topics:
        kw.append((cluster,
                   list(map(lambda x: x[0], sorted(kw_extractor.extract_keywords(topic), reverse=True, key=lambda y: y[1])))))
    return kw


def get_topics_tfidf(df):
    topics = []
    kw = []
    clusters = list(df["cluster"].unique())
    for cluster in clusters:
        topics.append((cluster, list(filter(lambda x: x != "", df[df['cluster'] == cluster]['text']))))
    vectorizer = TfidfVectorizer(stop_words="english")
    for cluster, topic in topics:
        try:
            X = vectorizer.fit_transform(topic)
            feature_array = np.array(vectorizer.get_feature_names_out())
            tfidf_sorting = np.argsort(X.toarray()).flatten()[::-1]
            top_n = feature_array[tfidf_sorting][:5]
            kw.append((cluster, top_n.tolist()))
        except Exception:
            kw.append((cluster, []))
    return kw


def get_embeddings(bertweet, tokenizer, tweets_text):
    tensors = [torch.tensor([tokenizer.encode(tweet, truncation=True)]) for tweet in tweets_text]
    features = []
    with torch.no_grad():
        for tensor in tensors:
            features.append(bertweet(tensor).pooler_output.tolist())
    features = list(map(lambda x: x[0], features))
    return features


def serialize_keywords(kws):
    return "|".join(list(map(lambda x: ",".join(x), kws)))


def calc_neighbour_distances(embeddings):
    neigh = NearestNeighbors(n_neighbors=2)
    nbrs = neigh.fit(embeddings)
    distances, indices = nbrs.kneighbors(embeddings)
    distances = np.sort(distances, axis=0)
    distances = distances[:,1]
    return distances


def run(exec_id):
    bertweet = AutoModel.from_pretrained("vinai/bertweet-base")
    tokenizer = AutoTokenizer.from_pretrained("vinai/bertweet-base", use_fast=False, model_max_length=128)
    tweets = session.query(Tweet).filter_by(exec_id=exec_id).all()
    user = session.query(User).filter_by(exec_id=exec_id).first()
    tweets_text = list(map(lambda x: x.text, tweets))
    df = pd.DataFrame(tweets_text, columns=['text'])
    features = get_embeddings(bertweet, tokenizer, tweets_text)
    umap_embeddings = umap.UMAP(metric='cosine').fit_transform(features) # Reduce dimensionality to perform better in clustering
    distances = calc_neighbour_distances(umap_embeddings)
    knee = KneeLocator(range(0, len(distances)), distances, S=1, curve='convex', direction='increasing')
    epsilon = distances[knee.knee]
    db = DBSCAN(eps=epsilon, metric='euclidean', min_samples=2).fit(umap_embeddings) # Fit DBSCAN classifier
    labels = db.labels_
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    noise_ = list(labels).count(-1)
    plot_clusters(labels, n_clusters_, db, umap_embeddings, exec_id)
    df['cluster'] = labels
    if len(list(df["cluster"].value_counts(sort=True))) >= 10:
        top_values = dict(zip(list(df["cluster"].value_counts(sort=True)[:10].index), list(df["cluster"].value_counts(sort=True)[:10])))
    else:
        top_values = dict(zip(list(df["cluster"].value_counts(sort=True).index), list(df["cluster"].value_counts(sort=True))))
    df["text"] = df["text"].map(lambda x: clean_tweet(x))
    topics = get_topics_tfidf(df)
    for cluster, topic in topics:
        if cluster in top_values.keys():
            topic_modeling = TopicModeling(exec_id, user.id, ",".join(topic), top_values[cluster])
            session.add(topic_modeling)
    session.add(TopicModeling(exec_id, user.id, "Noise", noise_))
    session.commit()


if __name__ == "__main__":
    run('51eef59a-9366-11ed-a95a-96c090691d1b')