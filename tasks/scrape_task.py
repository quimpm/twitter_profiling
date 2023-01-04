from time import sleep
from selenium.webdriver import Chrome, ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from tasks.twitter_scraper.scrape_profile import get_user_information
from tasks.twitter_scraper.scrape_tweet import get_tweet_information
from uuid import uuid1, UUID

#Main algorithm
def run(profile: str, exec_id: UUID):
    user_file = open("../data/user.csv", "a")
    tweets_file = open(f'../data/tweets/{exec_id}.csv', "w")
    options = ChromeOptions()
    options.add_argument('headless')
    options.add_argument('incognito')
    options.add_argument('window-size=1920x1080')
    options.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36")
    driver = Chrome(ChromeDriverManager().install(), chrome_options=options)
    driver.get("https://www.twitter.com/" + profile)
    sleep(15)
    user_info = get_user_information(driver)
    user_file.write(f'{exec_id},{user_info.to_csv()}')
    tweets_info = {}
    scrolling = True
    last_position = driver.execute_script("return window.pageYOffset;")
    curr_position = last_position + 3000
    while scrolling and len(tweets_info.values()) < 50:
        tweets = driver.find_elements('xpath', './/article[@data-testid="tweet"]')
        for tweet in tweets:
            try:
                scraped_tweet = get_tweet_information(driver, tweet)
            except Exception as e:
                print(e)
            if tweets_info.get(hash(scraped_tweet)) is None:
                tweets_info[hash(scraped_tweet)] = scraped_tweet
                tweets_file.write(scraped_tweet.to_csv())
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
    user_file.close()
    tweets_file.close()

if __name__ == "__main__":
    run("EvilAFM", uuid1())