from twitter_profiling.util import create_static_folder
from twitter_profiling.model.tweet import Tweet
from twitter_profiling.model.sentiment import Sentiment
from twitter_profiling.model.topic_modeling import TopicModeling
from twitter_profiling.db.db_session import session
from twitter_profiling import STATIC_FOLDER
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
import re
from wordcloud import WordCloud
from collections import Counter
import nltk


def plot_like_evolution(tweets, exec_id):
    plt.figure(figsize=(10, 10))
    d = {
        "likes": reversed(list(map(lambda x: x.likes, tweets))),
        "time": reversed(list(map(lambda x: x.time, tweets)))
    }
    df = pd.DataFrame(d)
    barplot = sns.lineplot(df, x="time", y="likes")
    barplot.set(title='Like Evolution')
    plt.xticks(rotation=90, fontsize=9)
    barplot.figure.savefig(STATIC_FOLDER+exec_id+"/likes")
    plt.clf()


def plot_views_evolution(tweets, exec_id):
    plt.figure(figsize=(10, 10))
    d = {
        "views": reversed(list(map(lambda x: x.views, tweets))),
        "time": reversed(list(map(lambda x: x.time, tweets)))
    }
    df = pd.DataFrame(d)
    barplot = sns.lineplot(df, x="time", y="views")
    barplot.set(title='Views Evolution')
    plt.xticks(rotation=90, fontsize=9)
    barplot.figure.savefig(STATIC_FOLDER + exec_id + "/views")
    plt.clf()


def plot_replies_evolution(tweets, exec_id):
    plt.figure(figsize=(10, 10))
    d = {
        "replies": reversed(list(map(lambda x: x.replies, tweets))),
        "time": reversed(list(map(lambda x: x.time, tweets)))
    }
    df = pd.DataFrame(d)
    barplot = sns.lineplot(df, x="time", y="replies")
    barplot.set(title='Replies evolution')
    plt.xticks(rotation=90, fontsize=9)
    barplot.figure.savefig(STATIC_FOLDER + exec_id + "/replies")
    plt.clf()


def plot_retweet_evolution(tweets, exec_id):
    plt.figure(figsize=(10, 10))
    d = {
        "retweets": reversed(list(map(lambda x: x.retweets, tweets))),
        "time": reversed(list(map(lambda x: x.time, tweets)))
    }
    df = pd.DataFrame(d)
    barplot = sns.lineplot(df, x="time", y="retweets")
    barplot.set(title='Retweet Evolution')
    plt.xticks(rotation=90, fontsize=9)
    barplot.figure.savefig(STATIC_FOLDER + exec_id + "/retweets")
    plt.clf()


def plot_sentiment_evolution(sentiment, tweets, exec_id):
    plt.figure(figsize=(10, 10))
    d = {
        "sentiment": reversed(list(map(lambda x: x.sentiment if x.label == "POSITIVE" else -x.sentiment, sentiment))),
        "time": reversed(list(map(lambda x: x.time, tweets)))
    }
    df = pd.DataFrame(d)
    barplot = sns.lineplot(df, x="time", y="sentiment")
    barplot.set(title='Sentiment Evolution')
    plt.xticks(rotation=90, fontsize=9)
    barplot.figure.savefig(STATIC_FOLDER + exec_id + "/sentiment")
    plt.clf()


def plot_topic_count(topics, exec_id):
    plt.figure(figsize=(10, 10))
    d = {
        "topic_count": list(map(lambda x: x.count, topics)),
        "topic": list(map(lambda x: x.id, topics))
    }
    df = pd.DataFrame(d)
    barplot = sns.barplot(df, x="topic", y="topic_count")
    barplot.set(title='Topic Tweet Count')
    barplot.figure.savefig(STATIC_FOLDER + exec_id + "/topics")
    plt.clf()


def plot_word_cloud(tweets, exec_id):
    corpus = ""
    lemmatizer = WordNetLemmatizer()
    for tweet in tweets:
        tweetStr = re.sub(r'[^\w]', ' ', tweet.text).lower()
        tweetStr = [word for word in tweetStr.split() if word not in stopwords.words('english')]
        tweetStr = [word[0] for word in pos_tag(tweetStr) if word[1] in ["NN", "NNS", "NNP", "NNPS"]]
        tweetStr = " ".join([lemmatizer.lemmatize(word) for word in tweetStr])
        corpus += tweetStr+" "
    wordcloud = WordCloud(max_font_size=50, max_words=200, background_color="white").generate(corpus)
    wordcloud.to_file(STATIC_FOLDER + exec_id + "/wordcloud.png")
    plt.clf()


def plot_usage_barplot(tweets, exec_id):
    count = dict(Counter(list(map(lambda x: x.time, tweets))))
    d = {"date": count.keys(), "count": count.values()}
    df = pd.DataFrame(d)
    barplot = sns.barplot(df, x="date", y="count")
    barplot.set(title='Topic Tweet Count')
    barplot.figure.savefig(STATIC_FOLDER + exec_id + "/usage")
    plt.clf()


def run(exec_id):
    nltk.download('stopwords')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('wordnet')
    create_static_folder(exec_id)
    tweets = session.query(Tweet).filter_by(exec_id=exec_id).all()
    sentiment = session.query(Sentiment).filter_by(exec_id=exec_id).all()
    topics = session.query(TopicModeling).filter_by(exec_id=exec_id).all()
    plot_like_evolution(tweets, exec_id)
    plot_retweet_evolution(tweets, exec_id)
    plot_sentiment_evolution(sentiment, tweets, exec_id)
    plot_replies_evolution(tweets, exec_id)
    plot_views_evolution(tweets, exec_id)
    plot_topic_count(topics, exec_id)
    plot_word_cloud(tweets, exec_id)
    plot_usage_barplot(tweets, exec_id)

if __name__ == "__main__":
    run('51eef59a-9366-11ed-a95a-96c090691d1b')