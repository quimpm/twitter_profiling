import sqlite3
from twitter_profiling import DB_HOST

if __name__ == "__main__":
    con = sqlite3.connect(DB_HOST)
    con.execute(
        "CREATE TABLE execution(id integer primary key not null, exec_id str, date text, target text)"
    )
    con.execute(
        "CREATE TABLE user(id integer primary key not null, exec_id str, name text, at text, desc text, profile_img text, banner_img text, geolocation text, join_date text, following integer, followers integer)"
    )
    con.execute(
        "CREATE TABLE tweet(id integer primary key not null, exec_id str, user_id integer, username text, at text, text text, views integer, replies integer, retweets integer, likes integer, imgs text, video text, link text, time text)"
    )
    con.execute(
        "CREATE TABLE tweet_sentiment(id integer primary key not null, exec_id str, tweet_id integer, sentiment integer, label text)"
    )
    con.execute(
        "CREATE TABLE statistics(id integer primary key not null, exec_id str, user_id integer, like_count integer, view_count integer, replies_count integer, retweet_count integer, most_viewed integer, most_liked integer, most_replied integer, most_retweeted integer, average_sentiment float, average_likes float, average_views float, average_replies float, average_retweets float)"
    )
    con.execute(
        "CREATE TABLE topic_modeling(id integer primary key not null, exec_id str, user_id integer, topic string, count integer)"
    )
