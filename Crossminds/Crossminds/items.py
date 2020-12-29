# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


# class MongoDB():
#     def __init__(self):
#         client = pymongo.MongoClient(LOCAL_MONGO_HOST, LOCAL_MONGO_PORT)
#         db = client[DB_NAME]
#         self.page = db['crossminds']

#     @staticmethod
#     def insert_item(collection, item):
#         try:
#             collection.update(dict(item),dict(item),upsert=True)
#         except DuplicateKeyError:
#             print("重复数据")
#             """
#             说明有重复数据
#             """


class CrossmindsItem(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    authors = scrapy.Field()
    abstract = scrapy.Field()
    publicationOrg = scrapy.Field()
    year = scrapy.Field()
    pdfUrl = scrapy.Field()
    pdfPath = scrapy.Field()
    publicationUrl = scrapy.Field()
    codeUrl = scrapy.Field()
    videoUrl = scrapy.Field()
    videoPath = scrapy.Field()
    description = scrapy.Field()
    source = scrapy.Field()
    pass
