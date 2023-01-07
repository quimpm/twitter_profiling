from twitter_profiling.db.db_session import Base
from sqlalchemy import Column, Integer, String


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    exec_id = Column(String)
    name = Column(String)
    at = Column(String)
    desc = Column(String)
    profile_img = Column(String)
    banner_img = Column(String)
    geolocation = Column(String)
    join_date = Column(String)
    following = Column(Integer)
    followers = Column(Integer)

    def __int__(self, exec_id, name, at, desc, profile_img, banner_img, geolocation, join_date, following, followers):
        self.exec_id = exec_id
        self.name = name
        self.at = at
        self.desc = desc.replace("\n", " ").replace(",", " ").replace("  ", " ")
        self.profile_img = profile_img
        self.banner_img = banner_img
        self.geolocation = geolocation
        self.join_date = join_date
        self.following = following
        self.followers = followers

    def __hash__(self):
        return hash(f'{self.exec_id}{self.name}{self.at}{self.desc}{self.profile_img}{self.banner_img}{self.geolocation}{self.join_date}{str(self.following)}{str(self.followers)}')
