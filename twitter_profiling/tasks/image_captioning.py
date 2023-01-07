from transformers import pipeline
from twitter_profiling.model.tweet import Tweet
from twitter_profiling.model.image_caption import ImageCaption
from twitter_profiling.db.db_session import session


def run(exec_id):
    image_to_text = pipeline("image-to-text", model="nlpconnect/vit-gpt2-image-captioning")
    tweets = session.query(Tweet).filter_by(exec_id=exec_id).all()
    for tweet in tweets:
        for img in tweet.imgs.split('|'):
            if img:
                caption = ImageCaption(exec_id, tweet.id, image_to_text(img)[0]['generated_text'])
                session.add(caption)
    session.commit()


if __name__ == "__main__":
    run('8027d0e6-8ea5-11ed-9424-96c090691d1b')