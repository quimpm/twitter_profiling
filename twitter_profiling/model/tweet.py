from twitter_profiling.db.db_session import Base
from sqlalchemy import Column, Integer, String


class Tweet(Base):
    __tablename__ = 'tweet'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    exec_id = Column(String)
    username = Column(String)
    at = Column(String)
    text = Column(String)
    views = Column(Integer)
    replies = Column(Integer)
    retweets = Column(Integer)
    likes = Column(Integer)
    imgs = Column(String)
    video = Column(String)
    link = Column(String)
    time = Column(String)

    def __init__(self, exec_id, user_id, username, at, text, views, replies, retweets, likes, imgs, video, link, time):
        self.exec_id = exec_id
        self.user_id = user_id
        self.username = username
        self.at = at
        self.text = text.replace("\n", " ").replace(",", " ").replace("  ", " ")
        self.views = views
        self.replies = replies
        self.retweets = retweets
        self.likes = likes
        self.imgs = "|".join(imgs)
        self.video = video
        self.link = link
        self.time = time

    def __hash__(self):
        return hash(f'{self.exec_id}{self.username}{self.at}{self.text}{str(self.views)}{str(self.replies)}{str(self.retweets)}{str(self.likes)}{self.imgs}{self.video}{self.link}{self.time}')
