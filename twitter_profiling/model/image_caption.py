from twitter_profiling.db.db_session import Base
from sqlalchemy import Column, Integer, String


class ImageCaption(Base):
    __tablename__ = 'image_caption'

    id = Column(Integer, primary_key=True)
    exec_id = Column(String)
    tweet_id = Column(Integer)
    caption = Column(String)

    def __init__(self, exec_id, tweet_id, caption):
        self.exec_id = exec_id
        self.tweet_id = tweet_id
        self.caption = caption
