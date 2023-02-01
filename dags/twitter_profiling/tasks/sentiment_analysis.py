from twitter_profiling.db.db_session import session
from twitter_profiling.model.tweet import Tweet
from twitter_profiling.model.sentiment import Sentiment
from transformers import pipeline, AutoTokenizer


def get_sentiment_analyzer(exec_id: str, tweet_id: int, text: str):
    """
    Perform sentiment analysis using RoBERTa model which has been carefully trained using milions of selected tweets
    :param exec_id: Correlation id of the execution
    :param tweet_id: Id of the tweet under analisys
    :param text: Text of the tweet under analysis
    :return:
    """
    roberta = 'cardiffnlp/twitter-roberta-base-sentiment'
    tokenizer = AutoTokenizer.from_pretrained(roberta)
    model = pipeline("sentiment-analysis", model=roberta, tokenizer=tokenizer)
    result = max(model(text), key=lambda x: x["score"])
    sentiment = Sentiment(exec_id=exec_id, tweet_id=tweet_id, sentiment=result["score"], label=result["label"])
    session.add(sentiment)


def run(exec_id: str):
    """
    Perform a sentiment analysis of a set of tweets
    :param exec_id: correlation id of the execution
    """
    tweets = session.query(Tweet).filter_by(exec_id=exec_id)
    for tweet in tweets:
        get_sentiment_analyzer(exec_id,tweet.id, tweet.text)
    session.commit()


if __name__ == "__main__":
    run('51eef59a-9366-11ed-a95a-96c090691d1b')
