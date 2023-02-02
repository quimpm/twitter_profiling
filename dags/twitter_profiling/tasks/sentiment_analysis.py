from twitter_profiling.db.db_session import session
from twitter_profiling.model.tweet import Tweet
from twitter_profiling.model.sentiment import Sentiment
from transformers import pipeline, AutoTokenizer
import urllib
import csv
from typing import Dict


def download_label_mapping():
    mapping_link = "https://raw.githubusercontent.com/cardiffnlp/tweeteval/main/datasets/sentiment/mapping.txt"
    with urllib.request.urlopen(mapping_link) as f:
        html = f.read().decode('utf-8').split("\n")
        csvreader = csv.reader(html, delimiter='\t')
    labels = {"LABEL_"+str(row[0]): row[1] for row in csvreader if len(row) > 1}
    return labels

def get_sentiment_analyzer(exec_id: str, tweet_id: int, text: str, labels: Dict[str,str], model):
    """
    Perform sentiment analysis using RoBERTa model which has been carefully trained using milions of selected tweets
    :param exec_id: Correlation id of the execution
    :param tweet_id: Id of the tweet under analisys
    :param text: Text of the tweet under analysis
    :return:
    """
    result = max(model(text), key=lambda x: x["score"])
    sentiment = Sentiment(exec_id=exec_id, tweet_id=tweet_id, sentiment=result["score"], label=labels[result["label"]])
    session.add(sentiment)


def run(exec_id: str):
    """
    Perform a sentiment analysis of a set of tweets
    :param exec_id: correlation id of the execution
    """
    labels = download_label_mapping()
    tweets = session.query(Tweet).filter_by(exec_id=exec_id)
    roberta = 'cardiffnlp/twitter-roberta-base-sentiment'
    tokenizer = AutoTokenizer.from_pretrained(roberta)
    model = pipeline("sentiment-analysis", model=roberta, tokenizer=tokenizer)
    for tweet in tweets:
        get_sentiment_analyzer(exec_id, tweet.id, tweet.text, labels, model)
    session.commit()


if __name__ == "__main__":
    run('51eef59a-9366-11ed-a95a-96c090691d1b')
