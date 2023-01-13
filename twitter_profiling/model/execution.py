from twitter_profiling.db.db_session import Base
from sqlalchemy import Column, Integer, String
from datetime import datetime


class Execution(Base):
    __tablename__ = 'execution'

    id = Column(Integer, primary_key=True)
    exec_id = Column(String)
    date = Column(String)
    target = Column(String)

    def __init__(self, exec_id, target):
        self.exec_id = exec_id
        self.date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.target = target
