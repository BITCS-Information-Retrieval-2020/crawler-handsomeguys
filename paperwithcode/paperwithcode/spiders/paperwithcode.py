import scrapy
from paperwithcode.items import PaperwithcodeItem
from scrapy.http import Request
import pymongo
import json
from paperwithcode.settings import FILE_STORED_PATH
import os
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError
import requests


class PaperWithCodeSpider(scrapy.Spider):

    name = "paperswithcode"

    def __init__(self):
        with open('./config.json') as f:
            config = json.load(f)
        self.config = config
        self.client = pymongo.MongoClient('mongodb://47.103.222.126:27017')
        db = self.client['crawler']
        db.authenticate('handsomeguys', '12138')
        self.collection = db['paperswithcode']

    def start_requests(self):
        page = int(self.config['page'])
        start_url = f'https://paperswithcode.com/api/v1/papers/?format=json&page={page}'
        yield Request(url=start_url, callback=self.parse, errback=self.errback)

    def parse(self, response):
        response_dict = json.loads(response.text)
        next_url = response_dict["next"]
        results = response_dict["results"]
        for paper in results:
            id = paper["id"]
            code_url_response = requests.get(
                f"https://paperswithcode.com/api/v1/papers/{id}/repositories")
            code_urls = json.loads(code_url_response.text)
            codeUrl = code_urls[0]["url"] if len(code_urls) > 0 else ""
            data = {
                "title":
                paper["title"],
                "authors":
                ", ".join(paper["authors"]),
                "abstract":
                paper["abstract"],
                "publicationOrg":
                paper["proceeding"] if paper["proceeding"] is not None else "",
                "year":
                paper["published"].split('-')[0]
                if paper["published"] is not None else "",
                "pdfUrl":
                paper["url_pdf"],
                "publicationUrl":
                paper["conference_url_pdf"]
                if paper["conference_url_pdf"] is not None else "",
                "codeUrl":
                codeUrl
            }
            if codeUrl != "":
                self.pdf_url.append(paper["url_pdf"])
            query = list(
                self.collection.find({}, {
                    "_id": 1
                }).sort('_id', -1).limit(1))
            data['_id'] = 1 if len(query) == 0 else query[0]['_id'] + 1
            self.collection.insert_one(data)
            if codeUrl != "":
                item = PaperwithcodeItem()
                item['title'] = response.meta['title']
                item['pdfContent'] = response.body
                yield item
        page = int(next_url.split("=")[-1])
        if page > self.config["page"]:
            # 当page大于上一个page值时表示爬虫未结束，更新config的page
            self.config["page"] = page
            yield Request(url=next_url, callback=self.parse)

    def errback(self, failure):
        # log all errback failures,
        # in case you want to do something special for some errors,
        # you may need the failure's type
        self.logger.error(repr(failure))

        if failure.check(HttpError):
            # you can get the response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)
            print('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)
            print('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)
            print('TimeoutError on %s', request.url)

    @staticmethod
    def close(spider, reason):
        with open('./config.json', 'w') as f:
            json.dump(spider.config, f)
        closed = getattr(spider, 'closed', None)
        if callable(closed):
            return closed(reason)
