from twitter_profiling.db.db_session import Base
from sqlalchemy import Column, Integer, String


class Sentiment(Base):
    __tablename__ = 'tweet_sentiment'

    id = Column(Integer, primary_key=True)
    exec_id = Column(String)
    tweet_id = Column(Integer)
    sentiment = Column(Integer)
    label = Column(String)

    def __init__(self, exec_id, tweet_id, sentiment, label):
        self.exec_id = exec_id
        self.tweet_id = tweet_id
        self.sentiment = sentiment
        self.label = label
