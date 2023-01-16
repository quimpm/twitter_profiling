from twitter_profiling.db.db_session import session
from twitter_profiling.model.tweet import Tweet
from twitter_profiling.model.sentiment import Sentiment
from transformers import pipeline


def get_sentiment_analyzer(exec_id, tweet_id, text):
    classifier = pipeline("sentiment-analysis")
    result = max(classifier(text), key=lambda x: x["score"])
    sentiment = Sentiment(exec_id=exec_id, tweet_id=tweet_id, sentiment=result["score"], label=result["label"])
    session.add(sentiment)


def run(exec_id):
    tweets = session.query(Tweet).filter_by(exec_id=exec_id)
    for tweet in tweets:
        get_sentiment_analyzer(exec_id,tweet.id, tweet.text)
    session.commit()


if __name__ == "__main__":
    run('51eef59a-9366-11ed-a95a-96c090691d1b')
