from time import sleep
from twitter_profiling.db.db_session import session
from twitter_profiling.model.tweet import Tweet
from selenium.webdriver import Chrome, ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from twitter_profiling.model.link_content import LinkContent


def run(exec_id: str):
    tweets = session.query(Tweet).filter_by(exec_id=exec_id).all()
    for tweet in tweets:
        if tweet.link:
            options = ChromeOptions()
            options.add_argument('headless')
            options.add_argument('incognito')
            options.add_argument('window-size=1920x1080')
            options.add_argument(
                "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36")
            driver = Chrome(ChromeDriverManager().install(), chrome_options=options)
            driver.get(tweet.link)
            sleep(15)
            text = driver.find_element('xpath', './/body').text
            link_content = LinkContent(exec_id=exec_id, tweet_id=tweet.id, link_content=text)
            session.add(link_content)
    session.commit()


if __name__ == "__main__":
    run('8027d0e6-8ea5-11ed-9424-96c090691d1b')