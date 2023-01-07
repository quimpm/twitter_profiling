import sqlite3
from twitter_profiling import DB_HOST

if __name__ == "__main__":
    con = sqlite3.connect(DB_HOST)
    con.execute(
        "CREATE TABLE execution(id integer primary key not null, exec_id str, date text, target text)"
    )
    con.execute(
        "CREATE TABLE user(id integer primary key not null, exec_id str, name text, at text, desc text, profile_img text, banner_img text, geolocation text, join_date text, following int, followers int)"
    )
    con.execute(
        "CREATE TABLE tweet(id integer primary key not null, exec_id str, user_id int, username text, at text, text text, views int, replies int, retweets int, likes int, imgs text, video text, link text, time text)"
    )
    con.execute(
        "CREATE TABLE tweet_sentiment(id integer primary key not null, exec_id str, tweet_id int, sentiment int)"
    )
    con.execute(
        "CREATE TABLE image_caption(id integer primary key not null, exec_id str, tweet_id int, caption text)"
    )
    con.execute(
        "CREATE TABLE link_content(id integer primary key not null, exec_id str, tweet_id int, link_content text)"
    )
    con.execute(
        "CREATE TABLE corpus(id integer primary key not null, exec_id str, user_id int, corpus text)"
    )
    con.execute(
        "CREATE TABLE statistics(id integer primary key not null, exec_id str, user_id int, like_count int, view_count int, replies_count int, retweet_count int, average_usage int, most_viewed int, most_liked int, most_discussed int, average_sentiment int)"
    )
    con.execute(
        "CREATE TABLE keywords(id integer primary key not null, exec_id str, user_id int, keywords text)"
    )
