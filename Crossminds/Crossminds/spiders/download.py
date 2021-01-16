import os
import re

import scrapy
from Crossminds.items import PDFItem
from Crossminds.settings import DEFAULT_REQUEST_HEADERS, FILES_STORE
from pymongo import MongoClient
from scrapy.crawler import CrawlerProcess
from scrapy.http import Request
from scrapy.utils.project import get_project_settings


class DownloadSpider(scrapy.Spider):
    name = 'download'

    def start_requests(self):
        yield Request(url='https://www.baidu.com/')

    def parse(self, response, **kwargs):
        client = MongoClient(
            'mongodb://handsomeguys:12138@47.103.222.126:27017/crawler')
        my_db = client['crawler']
        my_col = my_db['papers']

        queries = my_col.find({'pdfUrl': {
            '$ne': ''
        }}, {
            'title': 1,
            'pdfUrl': 1,
            'pdfPath': 1
        })
        for query in queries:
            _id, title, pdfUrl = query['_id'], query['title'], query['pdfUrl']

            pdf_name = re.sub(r'[^A-Za-z0-9_]', ' ', title)
            pdf_name = pdf_name.strip()
            pdf_name = re.sub(r'\s+', '_', pdf_name)

            pdfs = PDFItem()
            pdfs['file_names'] = pdf_name
            pdfs['file_urls'] = pdfUrl

            yield pdfs

            save_path = os.path.join(FILES_STORE, pdf_name + '.pdf')
            my_col.update_one({"_id": _id}, {"$set": {"pdfPath": save_path}})


if __name__ == "__main__":
    process = CrawlerProcess(get_project_settings())
    process.crawl(DownloadSpider)
    process.start()
