from twitter_profiling.db.db_session import session
from twitter_profiling.model.tweet import Tweet
from twitter_profiling.model.sentiment import Sentiment
from twitter_profiling.model.statistics import Statistics
from twitter_profiling.model.user import User
from typing import List, Tuple
from functools import reduce
from collections import Counter


def get_counts(tweets: List[Tweet]) -> Tuple[int, int, int, int]:
    """
    Count the total amount of views, likes, replies and retweets
    :param tweets:
    :return:
    """
    like_count, reply_count, retweet_count, view_count = 0, 0, 0, 0
    for tweet in tweets:
        like_count += tweet.likes
        reply_count += tweet.replies
        retweet_count += tweet.retweets
        view_count += tweet.views
    return like_count, reply_count, retweet_count, view_count


def get_maximums(tweets: List[Tweet]) -> Tuple[int, int, int, int]:
    """
    Retrieve tweets with best statistics of views, likes, replies and retweets
    :param tweets: Tweets of the user
    :return:
    """
    max_likes = max(tweets, key=lambda tweet: tweet.likes).id
    max_replies = max(tweets, key=lambda tweet: tweet.replies).id
    max_views = max(tweets, key=lambda tweet: tweet.views).id
    max_retweets = max(tweets, key=lambda tweet: tweet.retweets).id
    return max_likes, max_retweets, max_replies, max_views


def get_sentiment(tweets_sentiment: List[Sentiment]) -> int:
    """
    Calculate a sentiment score for the user
    :param tweets_sentiment: sentiment extracted from user tweets
    :return:
    """
    sentiment = list(map(lambda x: -x.sentiment if x.label == "NEGATIVE" else x.sentiment, tweets_sentiment))
    return reduce(lambda a, b: a+b, sentiment)


def get_usage(tweets: List[Tweet]) -> int:
    """
    Get the usage that the user performs of the platform
    :param tweets: Tweets of the user
    :return:
    """
    dates = dict(Counter(list(map(lambda x: x.time, tweets))))
    return reduce(lambda a,b: a+b, dates.values())/len(dates.keys())


def run(exec_id: str):
    """
    Task to calculate statistics based on the preprocessed information
    :param exec_id: correlation id of the execution
    :return:
    """
    tweets = session.query(Tweet).filter_by(exec_id=exec_id, is_retweeted=False).all()
    user = session.query(User).filter_by(exec_id=exec_id).first()
    tweets_sentiment = session.query(Sentiment).filter_by(exec_id=exec_id).all()
    like_count, reply_count, retweet_count, view_count = get_counts(tweets)
    like_avg, reply_avg, retweet_avg, view_avg = like_count/len(tweets), reply_count/len(tweets), retweet_count/len(tweets), view_count/len(tweets)
    max_likes, max_retweets, max_replies, max_views = get_maximums(tweets)
    avg_usage = get_usage(tweets)
    sentiment = get_sentiment(tweets_sentiment)
    statistics = Statistics(exec_id, user.id, like_count, view_count, reply_count, retweet_count, max_views, max_likes, max_replies, max_retweets, sentiment, like_avg, view_avg, reply_avg, retweet_avg, avg_usage)
    session.add(statistics)
    session.commit()


if __name__ == "__main__":
    run('51eef59a-9366-11ed-a95a-96c090691d1b')