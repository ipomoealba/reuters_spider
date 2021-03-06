# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ReutersItem(scrapy.Item):
    # define the fields for your item here like:
    publish_date = scrapy.Field()
    article_section = scrapy.Field()
    article_headline = scrapy.Field()
    article_text = scrapy.Field()
