from twitter_profiling.db.db_session import Base
from sqlalchemy import Column, Integer, String


class LinkContent(Base):
    __tablename__ = 'link_content'

    id = Column(Integer, primary_key=True)
    exec_id = Column(String)
    tweet_id = Column(Integer)
    link_content = Column(String)

    def __init__(self, exec_id, tweet_id, link_content):
        self.exec_id = exec_id
        self.tweet_id = tweet_id
        self.link_content = link_content
