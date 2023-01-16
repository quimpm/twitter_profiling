from snscrape.modules.twitter import TwitterUserScraper, Photo
from uuid import uuid1, UUID
from twitter_profiling.model.user import User
from twitter_profiling.model.tweet import Tweet
from twitter_profiling.db.db_session import session
from twitter_profiling.util import translate_text


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
            session.flush()
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


def scrape_tweets(user, exec_id, n_tweets, scraper):
    tweets = scraper.get_items()
    for i in range(n_tweets):
        tweet_scraped = next(tweets)
        tweet = Tweet(
            exec_id,
            user.id,
            tweet_scraped.user.displayname,
            tweet_scraped.user.username,
            translate_text(tweet_scraped.content),
            tweet_scraped.viewCount if tweet_scraped is not None else 0,
            tweet_scraped.replyCount,
            tweet_scraped.retweetCount,
            tweet_scraped.likeCount,
            parse_images(tweet_scraped.media),
            parse_links(tweet_scraped.links),
            tweet_scraped.date.strftime("%Y-%m-%d"),
            not user.at == tweet_scraped.username
        )
        session.add(tweet)


#Main algorithm
def run(profile: str, exec_id: str, n_tweets: str):
    n_tweets = int(n_tweets)
    scraper = TwitterUserScraper(profile)
    user = get_user(str(exec_id), scraper, profile)
    scrape_tweets(user, str(exec_id), n_tweets, scraper)
    session.commit()
    print("Job done")


if __name__ == "__main__":
    run("unclebobmartin", str(uuid1()), "100")
