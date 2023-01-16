from twitter_profiling.util import scrape_wrapper, parse_twitter_number


def get_username_and_date(driver, scraped_tweet):
    user_name = scraped_tweet.find_element('xpath', './/div[@data-testid="User-Names"]')
    values = user_name.text.splitlines()
    return values[0], values[1], values[3].replace(",","")


def get_text(driver, scraped_tweet):
    text = scraped_tweet.find_element('xpath', './/div[@data-testid="tweetText"]')
    return text.text


def get_reply(driver, scraped_tweet):
    reply = scraped_tweet.find_element('xpath', './/div[@data-testid="reply"]').text
    return parse_twitter_number(reply.replace(",", "")) if reply else 0


def get_retweet(driver, scraped_tweet):
    retweet = scraped_tweet.find_element('xpath', './/div[@data-testid="retweet"]').text
    return parse_twitter_number(retweet.replace(",", "")) if retweet else 0


def get_like(driver, scraped_tweet):
    like = scraped_tweet.find_element('xpath', './/div[@data-testid="like"]').text
    return parse_twitter_number(like.replace(",", "")) if like else 0


def get_views(driver, scraped_tweet):
    views = scraped_tweet.find_element('xpath', './/div[@role="group"]/div/a').text
    return parse_twitter_number(views.replace(",", "")) if views else 0


def get_imgs(driver, scraped_tweet):
    imgs = scraped_tweet.find_elements('xpath', './/img[@alt="Image"]')
    return tuple([img.get_attribute("src") for img in imgs])


def get_link(driver, scraped_tweet):
    link = scraped_tweet.find_element('xpath', './/div[@data-testid="card.wrapper"]/div/a')
    return link.get_attribute("href")


def get_video(driver, scraped_tweet):
    video = scraped_tweet.find_element('xpath', './/video')
    return video.get_attribute("src")[5:]




def get_tweet_information(driver, scraped_tweet):
    username, at, time = scrape_wrapper(driver, '', get_username_and_date, (scraped_tweet,))
    text = scrape_wrapper(driver, '', get_text, (scraped_tweet,))
    replies = scrape_wrapper(driver, 0, get_reply, (scraped_tweet,))
    retweets = scrape_wrapper(driver, 0, get_retweet, (scraped_tweet,))
    likes = scrape_wrapper(driver, 0, get_like, (scraped_tweet,))
    views = scrape_wrapper(driver, 0, get_views, (scraped_tweet,))
    imgs = scrape_wrapper(driver, (), get_imgs, (scraped_tweet,))
    link = scrape_wrapper(driver, '', get_link, (scraped_tweet,))
    video = scrape_wrapper(driver, '', get_video, (scraped_tweet,))
    return username, at, time, text, replies, retweets, likes, views, imgs, link, video
