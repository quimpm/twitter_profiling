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
    """
    Function to plot the clusters in a 2d graphic
    :param labels: List of clusters
    :param n_clusters_: Number of clusters
    :param db: dbscan algorithm
    :param umap_embeddings: 2D transformation of the BERTweet embedings
    :param exec_id: correlation id of the execution
    :return:
    """
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
    """
    Cleaning algorithm to perform KW and TF-IDF
    :param tweet: text of the tweet
    :return: text of the tweet cleaned
    """
    tweet = re.sub(r'@\w*', '', tweet).lower()
    tweet = demoji.replace(tweet, "")
    return re.sub(r'https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&\/=]*)', '', tweet)


def get_topics(df):
    """
    Keyword extraction using YAKE to extract the most relevant words from the clusters
    :param df: DataFrame containing the classification
    :return: List of top 5 keywords sorted by relevance
    """
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
    """
    Perform TF-IDF to the different clusters
    :param df: DataFrame containing the classification
    :return: List of top 5 keywords sorted by relevance
    """
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
    """
    Extract embedings from text using BERTweet
    :param bertweet: bertweet model
    :param tokenizer: tokenizer for fitting BERTweet model
    :param tweets_text: text that has to be transformed
    :return:
    """
    tensors = [torch.tensor([tokenizer.encode(tweet, truncation=True)]) for tweet in tweets_text]
    features = []
    with torch.no_grad():
        for tensor in tensors:
            features.append(bertweet(tensor).pooler_output.tolist())
    features = list(map(lambda x: x[0], features))
    return features


def serialize_keywords(kws):
    """
    Serialize the keywords for a certain topic to be storable
    :param kws: list of keywords
    :return: serialized string containing all keywords
    """
    return "|".join(list(map(lambda x: ",".join(x), kws)))


def calc_neighbour_distances(embeddings):
    """
    Perform nearest neighbours analisys for each point
    :param embeddings: Points in a 2d space
    :return: Minimum neighbour distances
    """
    neigh = NearestNeighbors(n_neighbors=2)
    nbrs = neigh.fit(embeddings)
    distances, indices = nbrs.kneighbors(embeddings)
    distances = np.sort(distances, axis=0)
    distances = distances[:,1]
    return distances


def run(exec_id: str):
    """
    Topic Extraction algorithm, the algorithm has the following steps:
    - Bert Embeddings:  Using the pretrained BERTweet model convert Tweets text to BERT embeddings (vectors).
                        Those vectors contain the all the information of the tweet text encoded.
    - UMAP:             UMAP is an algorithm to perform dimensionality reduction to high dimensional data that has similarities.
                        It's an algorithm able to convert n-dimensional datasets to 2-dimensional datasets, which
                        makes the work and analysis of the data a lot more easyer
    - NN:               Nearest neighbours analysis to get the distances from each point to the closest neighbour and order from lowest o biggest.
    - Knee:             Find the point of maximum curbature using kneed, this will be our epsilon parameter for DBSCAN.
    - DBSCAN:           Clustering using DB Scann algorithm. DBSCAN has been chosed as is an algorithm that does not require
                        pre vious knowledge on the dataset. IT has two main parameters that have been fine-tuned.
                        - epsilon:  Maximum distance from one point to another to be considered a neighbour.
                                    We set this as the point of maximum curbature of the nearest neighbours.
                        - min_pts:  Minimum number of points for a cluster to be considered a cluster.
                                    We set this to 2 as we want to get all possible clusters. After, we can filter by relevancy.
    - Plot Clusters:    Plot the generated clusters
    - TF-IDF/YAKE:      Get the most relevant words for each of the clusters to get the final topics. TF-IDF has been observed
                        to work better than YAKE.
    :param exec_id: correlation id of the execution
    :return:
    """
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
            topic_modeling = TopicModeling(exec_id, user.id, ",".join(topic), top_values[cluster], cluster)
            session.add(topic_modeling)
    session.add(TopicModeling(exec_id, user.id, "Noise", noise_, -1))
    session.commit()


if __name__ == "__main__":
    run('51eef59a-9366-11ed-a95a-96c090691d1b')