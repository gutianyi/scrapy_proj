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
#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 12/8/2020 9:15 下午
# @Author  : GU Tianyi
# @File    : model.py
import scrapy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, create_engine, Text, DateTime, Integer, String

class ZongyiItem(scrapy.Item):
    title = scrapy.Field()
    desc = scrapy.Field()
    times = scrapy.Field()
    page = scrapy.Field()

class GuoneiItem(scrapy.Item):
    title = scrapy.Field()
    desc = scrapy.Field()
    times = scrapy.Field()
    page = scrapy.Field()

class DianyingItem(scrapy.Item):
    title = scrapy.Field()
    desc = scrapy.Field()
    times = scrapy.Field()
    page = scrapy.Field()


class DataItem(scrapy.Item):
    title = scrapy.Field()
    desc = scrapy.Field()
    times = scrapy.Field()
    page = scrapy.Field()
    type = scrapy.Field()
