#                       _oo0oo_
#                      o8888888o
#                      88" . "88
#                      (| -_- |)
#                      0\  =  /0
#                    ___/`---'\___
#                  .' \\|     |// '.
#                 / \\|||  :  |||// \
#                / _||||| -:- |||||- \
#               |   | \\\  -  /// |   |
#               | \_|  ''\---/''  |_/ |
#               \  .-\__  '-'  ___/-. /
#             ___'. .'  /--.--\  `. .'___
#          ."" '<  `.___\_<|>_/___.' >' "".
#         | | :  `- \`.;`\ _ /`;.`/ - ` : | |
#         \  \ `_.   \_ __\ /__ _/   .-` /  /
#     =====`-.____`.___ \_____/___.-`___.-'=====
#                       `=---='
#
#                -*- coding: utf-8 -*-
#     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#               佛祖保佑         永无BUG
#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 17/8/2020 5:04 下午
# @Author  : GU Tianyi
# @File    : test.py

from selenium import webdriver
from pyquery import PyQuery as pq
import time

option = webdriver.ChromeOptions()
option.add_argument('headless')
option.add_argument('no-sandbox')
option.add_argument('--blink-setting=imagesEnabled=false')
browser = webdriver.Chrome(chrome_options=option)


def zhua(play_url):
    try:
        browser.get(play_url)
        audio = browser.find_element_by_class_name('music')
        time.sleep(2)#注意这个slee()
        return (audio.get_attribute('src'))
    finally:
        print()


def top(home_url):
    doc = pq(home_url)
    li = doc('.pc_temp_songlist.pc_rank_songlist_short ul li a.pc_temp_songname')
    for url in li.items():
        print(url.attr.href, url.attr('title') + '-----' + zhua(url.attr.href))


if __name__ == '__main__':
    url = "http://www.kugou.com/yy/rank/home/1-6666.html?from=homepage"
    top(url)