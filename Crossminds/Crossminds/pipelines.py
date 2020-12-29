# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from pymongo.errors import DuplicateKeyError
from scrapy.pipelines.files import FilesPipeline
from scrapy.http.request import Request

from Crossminds.items import CrossmindsItem, PDFItem


class CrossmindsPipeline(object):
    def __init__(self):
        # client = pymongo.MongoClient('mongodb://handsomeguys:12138@' + LOCAL_MONGO_HOST +':'+ str(LOCAL_MONGO_PORT)+'/')
        client = pymongo.MongoClient('mongodb://47.103.222.126:27017')
        # 'mongo --host 47.103.222.126 -u handsomeguys -p 12138 --authenticationDatabase crawler'
        db = client.crawler
        db.authenticate('handsomeguys', '12138')
        # db = client[DB_NAME]
        self.PaperSpiderItem = db['test']

    def process_item(self, item, spider):
        """ 判断item的类型，并作相应的处理，再入数据库 """
        if isinstance(item, CrossmindsItem):
            self.insert_item(self.PaperSpiderItem, item)
        return item

    @staticmethod
    def insert_item(collection, item):
        insert_data = dict(item)

        query = list(collection.find({}, {"_id": 1}).sort('_id', -1).limit(1))
        insert_data['_id'] = 1 if len(query) == 0 else query[0]['_id'] + 1

        collection.insert(insert_data)
        # 怎么判断数据库里有没有重复
        # try:
        #     collection.insert(dict(item))
        # except DuplicateKeyError as e:
        #     """
        #     说明有重复数据
        #     """
        #     print(e)


class PDFPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        if isinstance(item, PDFItem):
            yield Request(url=item['file_urls'], meta={'item': item})

    def file_path(self, request, response=None, info=None, *, item=None):
        file_name = item['file_name']
        return file_name + '.pdf'
