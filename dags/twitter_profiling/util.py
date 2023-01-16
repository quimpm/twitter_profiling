from time import sleep
import os
from twitter_profiling import STATIC_FOLDER
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from easynmt import EasyNMT


def get_language(text):
    tokenizer = AutoTokenizer.from_pretrained("papluca/xlm-roberta-base-language-detection")
    model = AutoModelForSequenceClassification.from_pretrained("papluca/xlm-roberta-base-language-detection")
    lang_classifier = pipeline("text-classification", model=model, tokenizer=tokenizer)
    return max(lang_classifier(text[:512]), key=lambda x: x["score"])["label"]


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


def create_static_folder(exec_id):
    if not os.path.exists(STATIC_FOLDER+exec_id):
        os.mkdir(STATIC_FOLDER+exec_id)


def translate_text(text):
    model = EasyNMT('opus-mt')
    try:
        return model.translate(text, target_lang="en")
    except:
        return text
