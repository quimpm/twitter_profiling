from twitter_profiling.db.db_session import Base
from sqlalchemy import Column, Integer, String


class TopicModeling(Base):
    __tablename__ = 'topic_modeling'

    id = Column(Integer, primary_key=True)
    exec_id = Column(String)
    user_id = Column(Integer)
    topic = Column(String)
    count = Column(Integer)
    cluster_id = Column(Integer)

    def __init__(self, exec_id, user_id, topic, count, cluster_id):
        self.exec_id = exec_id
        self.user_id = user_id
        self.topic = topic
        self.count = count
        self.cluster_id = cluster_id
