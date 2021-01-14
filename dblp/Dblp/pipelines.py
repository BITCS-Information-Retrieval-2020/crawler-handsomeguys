# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
import random

from scrapy.http.request import Request

import pymongo
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import unicodedata
import string
import scrapy
from scrapy.pipelines.files import FilesPipeline
from scrapy.settings.default_settings import DEFAULT_REQUEST_HEADERS

from .items import DblpItem, PDFItem


class CrossmindsPipeline:
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri='mongodb://47.103.222.126:27017',
            mongo_db='crawler'
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.db.authenticate('handsomeguys', '12138')
        self.collection = 'Dblp'

    def process_item(self, item, spider):
        print("--------------------")
        print(dict(item))
        print("-over----------")
        if isinstance(item, DblpItem):
            self.db[self.collection].insert(dict(item))
        else:
            print(item)
        return item

    def close_spider(self, spider):
        self.client.close()


class PDFPipeline(FilesPipeline):
    my_headers = [
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/39.0.2171.95 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/35.0.1916.153 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) \
        Version/7.0.3 Safari/537.75.14",
        "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
        'Opera/9.25 (Windows NT 5.1; U; en)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
        'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
        'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security \
        Firefox/1.5.0.12',
        'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
        "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 \
        Chrome/16.0.912.77 Safari/535.7",
        "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 "
    ]

    def get_media_requests(self, item, info):
        if isinstance(item, DblpItem):
            yield Request(url=item['pdfUrl'], headers=DEFAULT_REQUEST_HEADERS, meta={'title': item['title']})

    def file_path(self, request, response=None, info=None, *, item=None):
        file_name = request.meta['title']

        return file_name + '.pdf'

    def item_completed(self, results, item, info):
        if isinstance(item, DblpItem):
            print(results, item['pdfUrl'])
            item['pdfPath'] = "/data/PDFS/" + item['title']
        return item
