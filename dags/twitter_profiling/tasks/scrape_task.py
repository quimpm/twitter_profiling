from snscrape.modules.twitter import TwitterUserScraper, Photo
from uuid import uuid1, UUID
from twitter_profiling.model.user import User
from twitter_profiling.model.tweet import Tweet
from twitter_profiling.db.db_session import session
from easynmt import EasyNMT
from twitter_profiling import CACHE_FOLDER
import psutil


def translate_text(text, model):
    try:
        return model.translate(text, target_lang="en")
    except:
        return text


def get_user(exec_id, scraper, target):
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


def parse_images(medias):
    if medias is None:
        return ""
    elif len(medias) == 1:
        return medias[0].fullUrl if isinstance(medias[0], Photo) else ""
    else:
        return "|".join([media.fullUrl if isinstance(media, Photo) else "" for media in medias])


def parse_links(links):
    if links is None:
        return ""
    elif len(links) == 1:
        return links[0].url
    else:
        return "|".join([link.url for link in links])


def scrape_tweets(user, exec_id, n_tweets, scraper, translate):
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
        session.add(tweet)
        session.commit()
        print(psutil.virtual_memory())


#Main algorithm
def run(profile: str, exec_id: str, n_tweets: str, translate str):
    n_tweets = int(n_tweets)
    translate = translate == "True"
    scraper = TwitterUserScraper(profile)
    user = get_user(str(exec_id), scraper, profile)
    scrape_tweets(user, str(exec_id), n_tweets, scraper, translate)
    session.commit()


if __name__ == "__main__":
    run("unclebobmartin", str(uuid1()), "100")
