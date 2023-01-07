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
        "CREATE TABLE tweet_sentiment(id integer primary key not null, exec_id str, tweet_id integer, sentiment integer)"
    )
    con.execute(
        "CREATE TABLE image_caption(id integer primary key not null, exec_id str, tweet_id integer, caption text)"
    )
    con.execute(
        "CREATE TABLE link_content(id integer primary key not null, exec_id str, tweet_id int, link_content text)"
    )
    con.execute(
        "CREATE TABLE corpus(id integer primary key not null, exec_id str, user_id int, corpus text)"
    )
    con.execute(
        "CREATE TABLE statistics(id integer primary key not null, exec_id str, user_id integer, like_count integer, view_count integer, replies_count integer, retweet_count integer, average_usage integer, most_viewed integer, most_liked integer, most_discussed integer, average_sentiment integer, average_likes integer, average_replies integer, average_replies integer, average_retweets integer)"
    )
    con.execute(
        "CREATE TABLE keywords(id integer primary key not null, exec_id str, user_id integer, keywords text)"
    )
