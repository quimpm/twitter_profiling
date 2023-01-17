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


def get_topics(df, n_clusters_):
    topics = []
    kw = []
    for i in range(n_clusters_):
        topics.append(" ".join(list(df[df['cluster'] == i]['text'])))
    kw_extractor = yake.KeywordExtractor(n=2, top=5)
    for topic in topics:
        kw.append(list(map(lambda x: x[0], sorted(kw_extractor.extract_keywords(topic), reverse=True, key=lambda y: y[1]))))
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


def run(exec_id):
    bertweet = AutoModel.from_pretrained("vinai/bertweet-base")
    tokenizer = AutoTokenizer.from_pretrained("vinai/bertweet-base", use_fast=False, model_max_length=128)
    tweets = session.query(Tweet).filter_by(exec_id=exec_id).all()
    user = session.query(User).filter_by(exec_id=exec_id).first()
    tweets_text = list(map(lambda x: x.text, tweets))
    df = pd.DataFrame(tweets_text, columns=['text'])
    features = get_embeddings(bertweet, tokenizer, tweets_text)
    umap_embeddings = umap.UMAP(metric='cosine').fit_transform(features) # Reduce dimensionality to perform better in clustering
    db = DBSCAN(eps=0.35, metric='euclidean', min_samples=4).fit(umap_embeddings) # Fit DBSCAN classifier
    labels = db.labels_
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    n_tweets_topic = []
    for i in range(n_clusters_):
        n_tweets_topic.append(list(labels).count(i))
    noise_ = list(labels).count(-1)
    plot_clusters(labels, n_clusters_, db, umap_embeddings, exec_id)
    df['cluster'] = labels
    topics = get_topics(df, n_clusters_)
    for i, topic in enumerate(topics):
        topic_modeling = TopicModeling(exec_id, user.id, ",".join(topic), n_tweets_topic[i])
        session.add(topic_modeling)
    session.add(TopicModeling(exec_id, user.id, "Others", noise_))
    session.commit()


if __name__ == "__main__":
    run('51eef59a-9366-11ed-a95a-96c090691d1b')