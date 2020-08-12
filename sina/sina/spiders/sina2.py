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
#
#     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#               佛祖保佑         永无BUG
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 1/8/2020 10:40 上午
# @Author  : GU Tianyi
# @File    : sina2.py
import csv

import scrapy
from scrapy import Request
from scrapy.selector import Selector
from selenium import webdriver
from ..items import ZongyiItem,GuoneiItem,DianyingItem


class Sina2Spider(scrapy.Spider):
    name = 'sina'
    allowed_domains = ['sina.com.cn']

    def __init__(self, *args, **kwargs):
        # self.engine =
        super(Sina2Spider, self).__init__(*args, **kwargs)
        self.page = 10
        self.flag = 0
        self.start_urls = [
                            'https://ent.sina.com.cn/film/',
                            'https://ent.sina.com.cn/zongyi/',
                           'https://news.sina.com.cn/china/',
                           # 'https://fashion.sina.com.cn/'
                           ]
        self.option = webdriver.ChromeOptions()
        self.option.add_argument('headless')
        self.option.add_argument('no-sandbox')
        self.option.add_argument('--blink-setting=imagesEnabled=false')

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        driver = webdriver.Chrome(chrome_options=self.option)
        driver.set_page_load_timeout(60)
        driver.get(response.url)
        for i in range(self.page):
            while not driver.find_element_by_xpath("//div[@class='feed-card-page']").text:
                driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            count = driver.find_elements_by_xpath("//h2[@class='undefined']/a[@target='_blank']")

            for eachone in count:
                title = eachone.text
                if response.url == 'https://ent.sina.com.cn/zongyi/':
                    item = ZongyiItem()
                elif response.url == 'https://news.sina.com.cn/china/':
                    item = GuoneiItem()
                else:
                    item = DianyingItem()

                item['title'] = title
                item['desc'] = ''
                item['page'] = i+1
                href = eachone.get_attribute('href')
                yield Request(url=response.urljoin(href), meta={'name':item},callback=self.parse_namedetail)
            # driver.find_element_by_xpath("//div[@class='feed-card-page']/span[@class='pagebox_next']/a").click
            loc = driver.find_element_by_xpath("//div[@class='feed-card-page']/span[@class='pagebox_next']/a")
            driver.execute_script("arguments[0].click();", loc)


    def parse_namedetail(self, response):
        selector = Selector(response)
        time = selector.xpath("//div[@class='date-source']/span[@class='date']/text()").extract()
        desc = selector.xpath("//div[@class='article']/p/text()").extract()
        item = response.meta['name']



        t = time[0]
        item['desc'] = desc
        item['times'] = t
        yield item

