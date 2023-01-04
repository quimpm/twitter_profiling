from util import scrape_wrapper, parse_twitter_number
from model.user import User


def get_banner_image(driver):
    banner_img = driver.find_element('xpath', './/img[@draggable="true"]')
    return banner_img.get_attribute("src")


def get_username_and_at(driver):
    user_name = driver.find_element('xpath', './/div[@data-testid="UserName"]')
    return user_name.text.splitlines()


def get_description(driver):
    user_desc = driver.find_element('xpath', './/div[@data-testid="UserDescription"]')
    return user_desc.text


def get_location(driver):
    user_location = driver.find_element('xpath', './/span[@data-testid="UserLocation"]')
    return user_location.text


def get_join_date(driver):
    user_join_date = driver.find_element('xpath', './/span[@data-testid="UserJoinDate"]')
    return user_join_date.text


def get_following(driver, at):
    user_following = driver.find_element('xpath', './/a[@href="/' + at[1:] + '/following"]')
    return parse_twitter_number(user_following.text.split()[0])


def get_followers(driver, at):
    user_followers = driver.find_element('xpath', './/a[@href="/' + at[1:] + '/followers"]')
    return parse_twitter_number(user_followers.text.split()[0])


def get_user_information(driver):
    user = User()
    user.name, user.at = scrape_wrapper(driver, '', get_username_and_at)
    user.banner_image = scrape_wrapper(driver, '', get_banner_image)
    user.profile_img = "https://www.twitter.com/" + user.at[1:] + "/photo"
    user.desc = scrape_wrapper(driver, '', get_description)
    user.geolocation = scrape_wrapper(driver, '', get_location)
    user.join_date = scrape_wrapper(driver, '', get_join_date)
    user.following = scrape_wrapper(driver, 0, get_following, (user.at,))
    user.followers = scrape_wrapper(driver, 0, get_followers, (user.at,))
    return user