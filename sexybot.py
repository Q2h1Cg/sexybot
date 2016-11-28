#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import random

import requests
import telegram
from lxml import html
from telegram.ext import Updater, CommandHandler


# logger
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# updater and dispatcher
updater = Updater(token="your_token_here")
dispatcher = updater.dispatcher


def fetch_haixiuzu():
    """
    抓取「害羞组」图片
    :return: 图片地址
    :rtype: str
    """
    start = random.randint(0, 5000)

    try:
        # 获取话题地址
        resp = requests.get("https://www.douban.com/group/haixiuzu/discussion?start={}".format(start), timeout=3)
        resp.close()
        dom = html.fromstring(resp.content)
        page_url = random.choice(dom.xpath("//table[@class='olt']/tr/td[@class='title']/a")).get("href")

        # 随机选择图片
        resp = requests.get(page_url, headers={"Referer": page_url}, timeout=3)
        resp.close()
        dom = html.fromstring(resp.content)

        return random.choice(dom.xpath("//div[@class='topic-figure cc']/img")).get("src")

    except Exception as ex:
        logging.error("fetch_haixiuzu error: {}".format(ex))
        return fetch_haixiuzu()


def fetch_xhamster():
    """
    抓取「XHAMSTER」视频
    :return: 视频标题、缩略图、地址
    :rtype: tuple
    """
    categories = (
        "chinese",
        "amateur",
        "anal",
        "asian",
        "beach",
        "big_boobs",
        "bisexuals",
        "ebony",
        "blowjobs",
        "british",
        "castings",
        "celebs",
        "creampie",
        "cuckold",
        "cumshots",
        "female_choice",
        "femdom",
        "french",
        "gangbang",
        "gays",
        "german",
        "grannies",
        "group",
        "hd_videos",
        "hairy",
        "handjobs",
        "hentai",
        "interracial",
        "japanese",
        "latin",
        "lesbians",
        "milfs",
        "massage",
        "masturbation",
        "matures",
        "men",
        "old_young",
        "public",
        "shemale",
        "squirting",
        "swingers",
        "teens",
        "vintage",
        "vr",
        "voyeur"
    )
    page = random.randint(1, 100)

    try:
        # 随机页面、随机视频
        resp = requests.get("https://xhamster.com/channels/new-{}-{}.html".format(random.choice(categories), page), timeout=3)
        resp.close()
        dom = html.fromstring(resp.content)
        video = random.choice(dom.xpath("//div[contains(@class, 'video')]/a"))

        # 获取标题、缩略图、地址
        title = video.xpath("img")[0].get("alt")
        pic = video.xpath("img")[0].get("src")
        addr = video.get("href")
        return title, pic, addr

    except Exception as ex:
        logging.error("fetch_xhamster error: {}".format(ex))
        return fetch_xhamster()


def help_(bot, update):
    """
    帮助信息
    """
    msg = """----==== [ HELP ] ====----
    1. /pic
    2. /video
-----==== [END] ====----
"""
    bot.sendMessage(chat_id=update.message.chat_id, text=msg)


def picture(bot, update):
    """
    图片
    """
    bot.sendPhoto(chat_id=update.message.chat_id, photo=fetch_haixiuzu())


def video(bot, update):
    """
    视频
    """
    title, pic, addr = fetch_xhamster()
    bot.sendMessage(chat_id=update.message.chat_id, text="<b>{}</b>".format(title), parse_mode=telegram.ParseMode.HTML)
    bot.sendPhoto(chat_id=update.message.chat_id, photo=pic)
    bot.sendMessage(chat_id=update.message.chat_id, text="<a href='{}'>Link</a>".format(addr), parse_mode=telegram.ParseMode.HTML)


# handler
help_handler = CommandHandler("help", help_)
picture_handler = CommandHandler("pic", picture)
video_handler = CommandHandler("video", video)


# register handler
dispatcher.add_handler(help_handler)
dispatcher.add_handler(picture_handler)
dispatcher.add_handler(video_handler)


updater.start_polling()
