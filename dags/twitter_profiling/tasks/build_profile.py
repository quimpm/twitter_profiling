from jinja2 import Environment, FileSystemLoader
from twitter_profiling import TEMPLATES_FOLDER, STATIC_FOLDER
from twitter_profiling.model.user import User
from twitter_profiling.model.topic_modeling import TopicModeling
from twitter_profiling.model.tweet import Tweet
from twitter_profiling.model.statistics import Statistics
from twitter_profiling.db.db_session import session


def run(exec_id):
    """
    Construct the profile reading the required computations from the previous steps and building the data structure
    that will be forwarded to the HTML template.
    :param exec_id: correlation id of the execution
    :return:
    """
    user = session.query(User).filter_by(exec_id=exec_id).first()
    topics = session.query(TopicModeling).filter_by(exec_id=exec_id).all()
    statistics = session.query(Statistics).filter_by(exec_id=exec_id).first()
    most_liked_tweet = session.query(Tweet).filter_by(id=statistics.most_liked).first()
    most_viewed_tweet = session.query(Tweet).filter_by(id=statistics.most_viewed).first()
    most_replied_tweet = session.query(Tweet).filter_by(id=statistics.most_replied).first()
    most_retweeted_tweet = session.query(Tweet).filter_by(id=statistics.most_retweeted).first()
    profile_filename = STATIC_FOLDER+exec_id+"/profile.html"
    environment = Environment(loader=FileSystemLoader(TEMPLATES_FOLDER))
    template = environment.get_template("profile.html")
    context = {
        "at": user.at,
        "name": user.name,
        "followers": user.followers,
        "following": user.following,
        "location": user.geolocation,
        "join_date": user.join_date,
        "profile_img": user.profile_img,
        "banner_img": user.banner_img,
        "topics": list(map(lambda x: x.topic, topics)),
        "description": user.desc,
        "counts": list(map(lambda x: x.count, topics)),
        "sentiment_score": statistics.average_sentiment,
        "likes_count": statistics.like_count,
        "avg_likes": statistics.average_likes,
        "views_count": statistics.view_count,
        "avg_views": statistics.average_views,
        "replies_count": statistics.replies_count,
        "avg_replies": statistics.average_replies,
        "retweet_count": statistics.retweet_count,
        "avg_retweet": statistics.average_retweets,
        "avg_usage": statistics.average_usage,
        "most_liked_images": most_liked_tweet.imgs.split("|") if most_liked_tweet.imgs else [],
        "most_liked_text": most_liked_tweet.text,
        "most_liked_likes": most_liked_tweet.likes,
        "most_viewed_images": most_viewed_tweet.imgs.split("|") if most_liked_tweet.imgs else [],
        "most_viewed_text": most_viewed_tweet.text,
        "most_viewed_views": most_viewed_tweet.views,
        "most_replied_images": most_replied_tweet.imgs.split("|") if most_liked_tweet.imgs else [],
        "most_replied_text": most_replied_tweet.text,
        "most_replied_replies": most_replied_tweet.replies,
        "most_retweeted_images": most_retweeted_tweet.imgs.split("|") if most_liked_tweet.imgs else [],
        "most_retweeted_text": most_retweeted_tweet.text,
        "most_retweeted_retweets": most_retweeted_tweet.retweets,
    }
    with open(profile_filename, mode="w", encoding="utf-8") as results:
        results.write(template.render(context))
        print(f"writed in {profile_filename}")

if __name__ == "__main__":
    run("51eef59a-9366-11ed-a95a-96c090691d1b")