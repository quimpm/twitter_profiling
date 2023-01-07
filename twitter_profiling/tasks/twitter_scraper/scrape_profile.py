from twitter_profiling.util import scrape_wrapper, parse_twitter_number


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
    name, at = scrape_wrapper(driver, '', get_username_and_at)
    banner_image = scrape_wrapper(driver, '', get_banner_image)
    profile_img = "https://www.twitter.com/" + at[1:] + "/photo"
    desc = scrape_wrapper(driver, '', get_description)
    geolocation = scrape_wrapper(driver, '', get_location)
    join_date = scrape_wrapper(driver, '', get_join_date)
    following = scrape_wrapper(driver, 0, get_following, (at,))
    followers = scrape_wrapper(driver, 0, get_followers, (at,))
    return name, at, banner_image, profile_img, desc, geolocation, join_date, following, followers