from dataclasses import dataclass

@dataclass(eq=True)
class User():
    name: str = None
    at: str = None
    desc: str = None
    profile_img: str = None
    banner_img: str = None
    geolocation: str = None
    join_date: str = None
    following: int = None
    followers: int = None

    def to_csv(self):
        breakline = "\n"
        return f'{self.name},{self.at},{self.desc.replace(breakline," ").replace(",", " ").replace("  ", " ")},{str(self.profile_img)},{self.banner_img},{self.geolocation},{self.join_date},{str(self.following)},{str(self.followers)}\n'

    @staticmethod
    def from_csv(tweet):
        name, at, desc, profile_img, banner_img, geolocation, join_date, following, followers = tweet.split(',')
        return User(name, at, desc, profile_img, banner_img, geolocation, join_date, int(following), int(followers))