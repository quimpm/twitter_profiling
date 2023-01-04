from time import sleep
import os


def scrape_wrapper(driver, default, func, args=None):
    retries = 3
    if args:
        list_args = list(args)
        list_args.insert(0, driver)
        args = tuple(list_args)
    else:
        args = (driver,)
    try:
        return func(*args)
    except:
        try:
            sleep(1)
            return func(*args)
        except:
            return default


def parse_twitter_number(num_str: str):
    if "K" in num_str:
        num_str = num_str.replace("K", "")
        num = int(float(num_str) * 1000)
    elif "M" in num_str:
        num_str = num_str.replace("M","")
        num = int(float(num_str) * 1000000)
    else:
        num_str = num_str.replace(",","")
        num = int(num_str)
    return num


def write_in_tmp(filename, content):
    if not os.path.exists("../data/tmp"):
        os.mkdir("../data/tmp")
    with open('../data/tmp/'+filename, "w") as tmp_file:
        tmp_file.write(content)
