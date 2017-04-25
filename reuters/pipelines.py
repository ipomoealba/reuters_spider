# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

from scrapy import log
from reuters.settings import MONGODB_SERVER, MONGODB_PORT, MONGODB_DB
from scrapy.exceptions import DropItem


class ReutersPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(
            MONGODB_SERVER,
            MONGODB_PORT
        )
        self.db = connection[MONGODB_DB]
        self.collection = self.db['tmp']

    def process_item(self, item, spider):
        self.collection = self.db['business']
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            self.collection.insert({'article_section': item['article_section'],
                                    'article_headline': item['article_headline'],
                                    'article_text': item['article_text'],
                                    'publish_date': item['publish_date'], })
            log.msg("[!] NewData added to MongoDB database!",
                    level=log.DEBUG, spider=spider)
        return item
