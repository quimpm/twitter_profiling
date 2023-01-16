from twitter_profiling.db.db_session import session
from twitter_profiling.model.tweet import Tweet
from twitter_profiling.model.sentiment import Sentiment
from twitter_profiling.model.statistics import Statistics
from twitter_profiling.model.user import User
from functools import reduce


def get_counts(tweets):
    like_count, reply_count, retweet_count, view_count = 0, 0, 0, 0
    for tweet in tweets:
        like_count += tweet.likes
        reply_count += tweet.replies
        retweet_count += tweet.retweets
        view_count += tweet.views
    return like_count, reply_count, retweet_count, view_count


def get_maximums(tweets):
    max_likes = max(tweets, key=lambda tweet: tweet.likes).id
    max_replies = max(tweets, key=lambda tweet: tweet.replies).id
    max_views = max(tweets, key=lambda tweet: tweet.views).id
    max_retweets = max(tweets, key=lambda tweet: tweet.retweets).id
    return max_likes, max_retweets, max_replies, max_views


def get_sentiment(tweets_sentiment):
    sentiment = list(map(lambda x: -x.sentiment if x.label == "NEGATIVE" else x.sentiment, tweets_sentiment))
    return reduce(lambda a, b: a+b, sentiment)


def run(exec_id):
    tweets = session.query(Tweet).filter_by(exec_id=exec_id, is_retweeted=False).all()
    user = session.query(User).filter_by(exec_id=exec_id).first()
    tweets_sentiment = session.query(Sentiment).filter_by(exec_id=exec_id, is_retweeted=False).all()
    like_count, reply_count, retweet_count, view_count = get_counts(tweets)
    like_avg, reply_avg, retweet_avg, view_avg = like_count/len(tweets), reply_count/len(tweets), retweet_count/len(tweets), view_count/len(tweets)
    max_likes, max_retweets, max_replies, max_views = get_maximums(tweets)
    sentiment = get_sentiment(tweets_sentiment)
    statistics = Statistics(exec_id, user.id, like_count, view_count, reply_count, retweet_count, max_views, max_likes, max_replies, max_retweets, sentiment, like_avg, view_avg, reply_avg, retweet_avg)
    session.add(statistics)
    session.commit()


if __name__ == "__main__":
    run('51eef59a-9366-11ed-a95a-96c090691d1b')