# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ErshoufangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #block = scrapy.Field()
    area = scrapy.Field()
    href = scrapy.Field()
    title = scrapy.Field()
    square = scrapy.Field()
    huxing = scrapy.Field()
    orientation = scrapy.Field()
    floor = scrapy.Field()
    price = scrapy.Field()
    view = scrapy.Field()
    time = scrapy.Field()
    tags = scrapy.Field()