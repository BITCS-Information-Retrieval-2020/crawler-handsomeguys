# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import pymongo

from pymongo.errors import DuplicateKeyError
from .settings import LOCAL_MONGO_PORT,LOCAL_MONGO_HOST,DB_NAME

class MongoDB():
    def __init__(self):
        client = pymongo.MongoClient(LOCAL_MONGO_HOST, LOCAL_MONGO_PORT)
        db = client[DB_NAME]
        self.page = db['crossminds']

    @staticmethod
    def insert_item(collection, item):
        try:
            collection.update(dict(item),dict(item),upsert=True)
        except DuplicateKeyError:
            print("重复数据")
            """
            说明有重复数据
            """



class CrossmindsItem(scrapy.Item):
    author_name = scrapy.Field()
    author_email = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    video_url = scrapy.Field()
    pass
