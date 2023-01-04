import time
from transformers import pipeline
import csv
from model.tweet import Tweet
from util import write_in_tmp


def run(exec_id):
    tweets = []
    image_to_text = pipeline("image-to-text", model="nlpconnect/vit-gpt2-image-captioning")
    csv_file = open('../data/tweets/'+exec_id+'.csv', "r+")
    for line in csv_file.readlines():
        print(line.replace('\n', ''))
        tweet = Tweet.from_csv(line.replace('\n', ''))
        tweet_img = []
        for img in tweet.imgs:
            if img:
                tweet_img.append(image_to_text(img)[0]['generated_text'])
        tweet.imgs = tweet_img
        tweets.append(tweet.to_csv())
    csv_file.close()
    csv_file = open('../data/tweets/' + exec_id + '.csv', "w")
    for tweet in tweets:
        csv_file.write(tweet)
    csv_file.close()


if __name__ == "__main__":
    run('8880a336-8c79-11ed-871c-96c090691d1c')