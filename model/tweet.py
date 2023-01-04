from dataclasses import dataclass


@dataclass(eq=True, unsafe_hash=True)
class Tweet():
    username: str = None
    at: str = None
    text: str = None
    views: int = None
    replies: int = None
    retweets: int = None
    likes: int = None
    imgs: (str) = None
    video: str = None
    link: str = None
    time: str = None

    def to_csv(self):
        breakline = "\n"
        return f'{self.username},{self.at},{self.text.replace(breakline, " ").replace(",", " ").replace("  ", " ")},{str(self.views)},{str(self.replies)},{str(self.retweets)},{str(self.likes)},{"|".join(self.imgs)},{self.video},{self.link},{self.time}\n'

    @staticmethod
    def from_csv(tweet):
        username, at, text, views, replies, retweets, likes, imgs, video, link, time = tweet.split(',')
        return Tweet(username, at, text, int(views), int(replies), int(retweets), int(likes), imgs.split('|'), video, link, time)
