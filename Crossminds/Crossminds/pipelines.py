# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from pymongo.errors import DuplicateKeyError
from scrapy.pipelines.files import FilesPipeline
from scrapy.http.request import Request
import re

from Crossminds.items import CrossmindsItem, PDFItem
from Crossminds.settings import DEFAULT_REQUEST_HEADERS


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
            yield Request(url=item['file_urls'], headers=DEFAULT_REQUEST_HEADERS, meta={'file_names': item['file_names']})

    def file_path(self, request, response=None, info=None, *, item=None):
        file_name = request.meta['file_names']
        file_name = re.sub(r'\[[\x00-\x7F]+]\s*', '', file_name)  # 去掉中括号
        file_name = re.sub(r'(\([\x00-\x7F]*\))', '', file_name)  # 去掉小括号
        file_name = file_name.strip()
        file_name = re.sub(r'[\s\-]+', '_', file_name)  # 空格和连接符转化为_
        file_name = re.sub(r'\W', '', file_name)  # 去掉所有奇怪的字符
        return file_name + '.pdf'

    def item_completed(self, results, item, info):
        print(results, item['file_urls'])
        return item
