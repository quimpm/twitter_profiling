from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from twitter_profiling import DB_HOST
import pathlib
from twitter_profiling.db import init_db

file = pathlib.Path(DB_HOST)
if not file.exists():
    init_db.run()
engine = create_engine('sqlite:///'+DB_HOST)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()
