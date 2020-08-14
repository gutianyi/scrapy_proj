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
import re
import datetime

import scrapy
from scrapy import Request
from scrapy.selector import Selector
from selenium import webdriver

from ..models.model import DataItem




class Sina2Spider(scrapy.Spider):
    name = 'sina'
    allowed_domains = ['sina.com.cn']

    def __init__(self, page=None, flag=None, *args, **kwargs):

        super(Sina2Spider, self).__init__(*args, **kwargs)
        self.page = int(page)
        self.flag = int(flag)
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
        for page in range(self.page):
            while not driver.find_element_by_xpath("//div[@class='feed-card-page']").text:
                driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            title = driver.find_elements_by_xpath("//h2[@class='undefined']/a[@target='_blank']")
            time = driver.find_elements_by_xpath("//h2[@class='undefined']/../div[@class='feed-card-a feed-card-clearfix']/div[@class='feed-card-time']")

            for i in range(len(title)):
                eachtitle = title[i].text
                eachtime = time[i].text
                item = DataItem()
                if response.url == 'https://ent.sina.com.cn/zongyi/':
                    item['type'] = 'zongyi'
                elif response.url == 'https://news.sina.com.cn/china/':
                    item['type'] = 'news'
                else:
                    item['type'] = 'film'


                item['title'] = eachtitle
                item['desc'] = ''
                item['page'] = page+1
                href = title[i].get_attribute('href')
                today = datetime.datetime.now()
                eachtime = eachtime.replace('今天',str(today.month) + '月' + str(today.day) + '日')
                if '分钟前' in eachtime:
                    minute = int(eachtime.split('分钟前')[0])
                    t = datetime.datetime.now() - datetime.timedelta(days=minute)
                    t2 = datetime.datetime(year=t.year, month=t.month, day=t.day,hour=t.hour, minute=t.minute)
                else:
                    if '年' not in eachtime:
                        eachtime = str(today.year) + '年' + eachtime
                    t1 = re.split('[年月日:]', eachtime)
                    t2 = datetime.datetime(year=int(t1[0]), month=int(t1[1]), day=int(t1[2]), hour=int(t1[3]),
                                       minute=int(t1[4]))

                item['times'] = t2

                if self.flag == 1:  # 增量爬取
                    today = datetime.datetime.now().strftime("%Y-%m-%d")
                    yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
                    if item['times'].strftime("%Y-%m-%d") < yesterday:
                        # self.crawler.engine.close_spider(self, "该条超出时间范围")
                        driver.close()
                        break
                    # 只取昨天发生的新闻事件
                    elif yesterday <= item['times'].strftime("%Y-%m-%d") < today:
                        yield Request(url=response.urljoin(href), meta={'name':item},callback=self.parse_namedetail)

                else:
                    yield Request(url=response.urljoin(href), meta={'name':item},callback=self.parse_namedetail)

            #跳出while 找到下一页标签
            try:
                driver.find_element_by_xpath("//div[@class='feed-card-page']/span[@class='pagebox_next']/a").click()
            except:
                break


    def parse_namedetail(self, response):
        selector = Selector(response)

        #进行解耦合
        desc = selector.xpath("//div[@class='article']/p/text()").extract()
        item = response.meta['name']
        desc = list(map(str.strip, desc))
        item['desc'] = ''.join(desc)
        yield item

