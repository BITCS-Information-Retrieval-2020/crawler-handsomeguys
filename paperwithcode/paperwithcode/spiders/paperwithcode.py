import scrapy
from paperswithcode import PapersWithCodeClient
from paperwithcode.items import PaperwithcodeItem
from scrapy.http import Request
import pymongo
import json
from paperwithcode.settings import FILE_STORED_PATH
import os


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
        client = PapersWithCodeClient()
        page = int(self.config['page'])
        while page is not None:
            try:
                papers = client.paper_list(page=page)
            except KeyError:
                page += 1
                papers = client.paper_list(page=page)
            for paper in papers.results:
                try:
                    repository = client.paper_repository_list(
                        paper_id=paper.id)[0]
                except IndexError:
                    repository = None
                if paper.conference is not None:
                    try:
                        conference = client.conference_get(
                            conference_id=paper.conference)
                    except BaseException:
                        conference = None
                else:
                    conference = None
                meta = {
                    "title":
                    paper.title,
                    "authors":
                    ", ".join(paper.authors),
                    "abstract":
                    paper.abstract,
                    "publicationOrg":
                    conference.name if conference is not None else "",
                    "year":
                    paper.published.year,
                    "pdfUrl":
                    paper.url_pdf,
                    "publicationUrl":
                    paper.conference_url_pdf
                    if paper.conference_url_pdf is not None else "",
                    "codeUrl":
                    repository.url if repository is not None else "",
                }
                query = list(
                    self.collection.find({}, {
                        "_id": 1
                    }).sort('_id', -1).limit(1))
                meta['_id'] = 1 if len(query) == 0 else query[0]['_id'] + 1
                self.collection.insert_one(meta)
                if repository is not None:
                    yield Request(
                        url=paper.url_pdf,
                        meta={
                            "title": paper.title,
                        },
                        callback=self.parse,
                        errback=self.errback,
                    )
            page = papers.next_page
            self.config['page'] = page

    def parse(self, response):
        item = PaperwithcodeItem()
        item['title'] = response.meta['title']
        item['pdfContent'] = response.body
        return item

    def errback(self, failure):
        self.logger.error(repr(failure))

    @staticmethod
    def close(spider, reason):
        with open('./config.json', 'w') as f:
            json.dump(spider.config, f)
        closed = getattr(spider, 'closed', None)
        if callable(closed):
            return closed(reason)
