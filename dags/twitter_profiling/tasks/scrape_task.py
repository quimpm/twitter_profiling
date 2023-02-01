from snscrape.modules.twitter import TwitterUserScraper, Photo, TextLink
from uuid import uuid1, UUID
from twitter_profiling.model.user import User
from twitter_profiling.model.tweet import Tweet
from twitter_profiling.db.db_session import session
from easynmt import EasyNMT
from twitter_profiling import CACHE_FOLDER
from typing import List
import psutil


def translate_text(text: str, model: EasyNMT) -> str:
    """
    Translate text from an autodetected language to english using EasyNMT library
    :param text: Text to be translated
    :param model: EasyNMT entity
    :return:
    """
    try:
        return model.translate(text, target_lang="en")
    except:
        return text


def get_user(exec_id: str, scraper: TwitterUserScraper, target: str) -> User:
    """
    Scrape the profile info from a user
    :param exec_id: correlation id of the execution
    :param scraper: Scraper Object
    :param target: User to be scraped
    """
    user = None
    tweets = scraper.get_items()
    for tweet in tweets:
        if tweet.username == target:
            user = User(
                exec_id,
                tweet.user.displayname,
                tweet.user.username,
                tweet.user.renderedDescription,
                tweet.user.profileImageUrl,
                tweet.user.profileBannerUrl,
                tweet.user.location,
                tweet.user.url,
                tweet.user.created.strftime("%Y-%m-%d"),
                tweet.user.friendsCount,
                tweet.user.followersCount
            )
            session.add(user)
            session.commit()
            break
    return user


def parse_images(medias: List[Photo]) -> str:
    """
    Serialize Snscrape Links type to a custom storable string
    :param medias: Images to be serialized
    """
    if medias is None:
        return ""
    elif len(medias) == 1:
        return medias[0].fullUrl if isinstance(medias[0], Photo) else ""
    else:
        return "|".join([media.fullUrl if isinstance(media, Photo) else "" for media in medias])


def parse_links(links: List[TextLink]) -> str:
    """
    Serialize Snscrape Links type to a custom storable string
    :param links: Links to be serialized
    """
    if links is None:
        return ""
    elif len(links) == 1:
        return links[0].url
    else:
        return "|".join([link.url for link in links])


def scrape_tweets(user: User, exec_id: str, n_tweets: int, scraper: TwitterUserScraper, translate: bool):
    """
    Scrape tweets of a profile using Snscrape
    :param user: user that is beeing scraped
    :param exec_id: correlation id of the execution
    :param n_tweets: number of tweets to extract
    :param scraper: Snscraper Entity
    :param translate: Flag to determine if translation is required
    """
    model = EasyNMT('opus-mt', max_loaded_models=3, cache_folder=CACHE_FOLDER)
    tweets = scraper.get_items()
    for i in range(n_tweets):
        tweet_scraped = next(tweets)
        tweet = Tweet(
            exec_id,
            user.id,
            tweet_scraped.user.displayname,
            tweet_scraped.user.username,
            translate_text(tweet_scraped.content, model) if translate else tweet_scraped.content,
            tweet_scraped.viewCount if tweet_scraped.viewCount is not None else 0,
            tweet_scraped.replyCount if tweet_scraped.replyCount is not None else 0,
            tweet_scraped.retweetCount if tweet_scraped.retweetCount is not None else 0,
            tweet_scraped.likeCount if tweet_scraped.likeCount is not None else 0,
            parse_images(tweet_scraped.media),
            parse_links(tweet_scraped.links),
            tweet_scraped.date.strftime("%Y-%m-%d"),
            not user.at == tweet_scraped.username
        )
        print(tweet)
        session.add(tweet)
        session.commit()
        print(psutil.virtual_memory())


def run(profile: str, exec_id: str, n_tweets: str, translate: bool):
    """
    Tweet scraping algorithm using Snscrape for scraping and EasyNMT for translating from
    autodetected language to english.
    :param profile: Profile to scrape
    :param exec_id: correlation id of the execution
    :param n_tweets: number of tweets to scrape
    :param translate: Apply translation
    """
    n_tweets = int(n_tweets)
    translate = translate == "True"
    scraper = TwitterUserScraper(profile)
    user = get_user(str(exec_id), scraper, profile)
    scrape_tweets(user, str(exec_id), n_tweets, scraper, translate)
    session.commit()


if __name__ == "__main__":
    run("unclebobmartin", str(uuid1()), "100", False)
