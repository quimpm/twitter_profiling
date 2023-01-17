from twitter_profiling.db.db_session import Base
from sqlalchemy import Column, Integer, String, Float


class Statistics(Base):
    __tablename__ = 'statistics'

    id = Column(Integer, primary_key=True)
    exec_id = Column(String)
    user_id = Column(Integer)
    like_count = Column(Integer)
    view_count = Column(Integer)
    replies_count = Column(Integer)
    retweet_count = Column(Integer)
    most_viewed = Column(Integer)
    most_liked = Column(Integer)
    most_replied = Column(Integer)
    most_retweeted = Column(Integer)
    average_sentiment = Column(Float)
    average_likes = Column(Float)
    average_views = Column(Float)
    average_replies = Column(Float)
    average_retweets = Column(Float)
    average_usage = Column(Float)

    def __init__(self, exec_id, user_id, like_count, view_count, replies_count, retweet_count, most_viewed, most_liked, most_replied, most_retweeted, average_sentiment, average_likes, average_views, average_replies, average_retweets, average_usage):
        self.exec_id = exec_id
        self.user_id = user_id
        self.like_count = like_count
        self.view_count = view_count
        self.replies_count = replies_count
        self.retweet_count = retweet_count
        self.most_viewed = most_viewed
        self.most_liked = most_liked
        self.most_replied = most_replied
        self.most_retweeted = most_retweeted
        self.average_sentiment = average_sentiment
        self.average_likes = average_likes
        self.average_views = average_views
        self.average_replies = average_replies
        self.average_retweets = average_retweets
        self.average_usage = average_usage


