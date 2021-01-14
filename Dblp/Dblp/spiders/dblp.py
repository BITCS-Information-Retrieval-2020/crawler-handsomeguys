import json

import scrapy
import requests
from scrapy.crawler import CrawlerProcess

from ..items import DblpItem, PDFItem

# from ..pipelines import DblpPipeline
# import pymysql
# from bs4 import BeautifulSoup
# from scrapy.crawler import CrawlerProcess
PAPER_PERPAGE = 500
KEYWORD_NUM = 50


class DblpSpider(scrapy.Spider):
    name = 'Dblp'

    # allowed_domains = ['Dblp.com']
    # start_urls = ['http://dblp.com/']
    def __init__(self):
        self.word_list = ["Transformer", "Bert", "LSTM", "attention"]
        self.word_list_tmp = ["Transformer", "Bert", "LSTM", "attention"]
        self.new_key_words = []

    def start_requests(self):
        # conn = pymysql.connect(host='192.168.1.8',
        #                        port=3306,
        #                        user='mywang88',
        #                        password='hahahaha',
        #                        db='Dblp')
        # cur = conn.cursor()
        # # 构造查询语句
        # sql = 'SELECT keyword FROM table_name'
        # # 执行查询语句
        # cur.execute(sql)
        # 提取查询结果
        # word_list = list(cur.fetchall())
        # 关闭连接
        # conn.close()

        keyword = self.word_list_tmp[0]
        # 构造 url
        # url = 'https://dblp.org/search?q='
        # url += keyword
        # url += '&h=1&format=json'
        self.word_list_tmp.pop(0)
        print("=== Key words to be crawl: ", self.word_list_tmp)
        url = 'https://dblp.uni-trier.de/search/publ/api?q='
        url += keyword
        url += '&h=' + str(PAPER_PERPAGE) + '&format=json'

        # 创建 scrapy.Request 实例
        req = scrapy.Request(url=url,
                             callback=self.parse)
        yield req

    # def parse(self, response):
    #     entres = response.css("li.entry")
    #     for entry in entres:
    #         item = DblpItem()
    #         pdf_url = entry.css("div.head a::attr(href)")[0].get()
    #         title = entry.css("span.title::text").get()
    #         paper_info = entry.css("span")
    #         authors = paper_info.css("span[itemprop='author'] span::text").getall()
    #         year = paper_info.css("span[itemprop='datePublished']::text").getall()
    #
    #         item["pdfUrl"] = pdf_url
    #         item["title"] = title
    #         item["authors"] = authors
    #         item["year"] = year
    #
    #         yield item

    def parse(self, response):
        result = json.loads(response.text)
        # print("===result:", result)
        try:
            tips = result['result']['hits']['hit']
        except KeyError:
            tips = []
        # print("===tips:", type(tips))
        listPrint = ["authors", "title", "venue", "year", "type", "key", "doi", "ee", "url"]
        not_crawl = ["type", "key", "doi", "url"]

        item = DblpItem()
        for tip in tips:
            for instance in listPrint:
                if instance in not_crawl:
                    continue
                if instance == 'authors':
                    # author
                    try:
                        authors = tip['info']['authors']['author']
                        # print("All authors: ", type(authors) == type({}))
                        if isinstance(authors, dict):
                            authors = [authors['text']]
                        else:
                            authors = [x["text"] for x in authors]
                        # authors = [x["text"] for x in authors]
                        # print(instance, ": ", authors)
                        item[instance] = authors
                    except KeyError:
                        item[instance] = ""

                else:
                    # print(instance, ": ", tips[0]['info'][instance])
                    if instance == "venue":
                        try:
                            item["publicationOrg"] = tip['info'][instance]
                        except KeyError:
                            item["publicationOrg"] = ""
                    elif instance == "ee":
                        try:
                            item["pdfUrl"] = tip['info'][instance]
                        except KeyError:
                            item["pdfUrl"] = ""
                    else:
                        try:
                            item[instance] = tip['info'][instance]
                        except KeyError:
                            item[instance] = ""
            # if len(item["pdfUrl"]) > 0:
            #     pdfUrl = item["pdfUrl"]
            #     req = scrapy.Request(url = pdfUrl, callback = self.pdfPaser)
            #     print("----pdfUrl: ", pdfUrl)
            #     print("----pdfDownloadUrl: ", req)
            #     yield req

            if len(self.word_list) <= KEYWORD_NUM:
                self.new_key_words = item["title"].split()
                for word in self.new_key_words:
                    if len(word) <= 3:
                        continue
                    if word not in self.word_list:
                        self.word_list.append(word)
                        self.word_list_tmp.append(word)
            print("=== Key words to be crawl: ", self.word_list_tmp)
            yield item

        if len(self.word_list_tmp) > 0:
            keyword = self.word_list_tmp[0]
            print("Start next crawl: ", self.word_list_tmp[0])
            self.word_list_tmp.pop(0)
            print("=== Key words to be crawl: ", self.word_list_tmp)

            url = 'https://dblp.uni-trier.de/search/publ/api?q='
            url += keyword
            url += '&h=' + str(PAPER_PERPAGE) + '&format=json'

            # 创建 scrapy.Request 实例
            req = scrapy.Request(url=url,
                                 callback=self.parse)
            yield req

    def pdfPaser(self, response):
        a = response.css('a').xpath('@href').getall()
        a = list(set(a))
        # print(a)
        for href in a:
            if ".pdf" in href and href[:4] == 'http':
                return {"pdfURL": href}
                # if self.downLoaderPdf:
                #     try:
                #         pdf_r = requests.get(href, stream="TRUE")
                #     except RuntimeError:
                #         continue
                #     print(href)

#
# process = CrawlerProcess(settings={
#     "FEEDS": {
#         "items.json": {"format": "json"},
#     },
# })
#
# process.crawl(DblpSpider)
# process.start()  # the script will block here until the crawling is finished
