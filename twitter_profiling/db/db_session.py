from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from twitter_profiling import DB_HOST

engine = create_engine('sqlite:///'+DB_HOST)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()
