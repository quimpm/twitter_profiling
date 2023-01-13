from time import sleep
from datetime import datetime
from selenium.webdriver import Chrome, ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from twitter_profiling.tasks.twitter_scraper.scrape_profile import get_user_information
from twitter_profiling.tasks.twitter_scraper.scrape_tweet import get_tweet_information
from uuid import uuid1, UUID
from twitter_profiling.model.user import User
from twitter_profiling.model.tweet import Tweet
from twitter_profiling.db.db_session import session


#Main algorithm
def run(profile: str, exec_id: UUID):
    print(datetime.now())
    options = ChromeOptions()
    options.add_argument('headless')
    options.add_argument('incognito')
    options.add_argument('window-size=1920x1080')
    options.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36")
    driver = Chrome(ChromeDriverManager().install(), chrome_options=options)
    driver.get("https://www.twitter.com/" + profile)
    sleep(15)
    name, at, banner_image, profile_img, desc, geolocation, join_date, following, followers = get_user_information(driver)
    user = User(exec_id=str(exec_id), name=name, at=at, banner_img=banner_image, profile_img=profile_img, desc=desc, geolocation=geolocation, join_date=join_date, following=following, followers=followers)
    session.add(user)
    session.flush()
    tweets_info = {}
    scrolling = True
    last_position = driver.execute_script("return window.pageYOffset;")
    curr_position = last_position + 3000
    while scrolling and len(tweets_info.values()) < 100:
        tweets = driver.find_elements('xpath', './/article[@data-testid="tweet"]')
        for tweet in tweets:
            try:
                username, at, time, text, replies, retweets, likes, views, imgs, link, video = get_tweet_information(driver, tweet)
                scraped_tweet = Tweet(exec_id=str(exec_id), user_id=user.id, username=username, at=at, time=time, text=text, replies=replies, retweets=retweets, likes=likes, views=views, imgs=imgs, link=link, video=video)
                if tweets_info.get(hash(scraped_tweet)) is None:
                    tweets_info[hash(scraped_tweet)] = scraped_tweet
                    session.add(scraped_tweet)
            except Exception as e:
                print(e)
        scroll_attempt = 0
        while True:
            driver.execute_script('window.scrollTo(0, '+str(curr_position)+');')
            if last_position == curr_position:
                scroll_attempt += 1
                if scroll_attempt >= 10:
                    scrolling = False
                    break
                else:
                    sleep(2)
            else:
                last_position = curr_position
                sleep(1)
                break
            curr_position = last_position + 2000
    session.commit()

if __name__ == "__main__":
    run("unclebobmartin", uuid1())