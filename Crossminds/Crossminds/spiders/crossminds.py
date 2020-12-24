# -*- coding: utf-8 -*-
import scrapy
import time
import json
from bs4 import BeautifulSoup
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from scrapy.http import Request,FormRequest
from Crossminds.settings import DEFAULT_REQUEST_HEADERS
from Crossminds.items import CrossmindsItem


class CrossmindsSpider(scrapy.Spider):
       name = 'Crossminds'
       start_url = 'https://api.crossminds.io/content/category/parents/details'


       def start_requests(self):

              yield Request(url=self.start_url, headers=DEFAULT_REQUEST_HEADERS, callback=self.parse)

       def parse(self, response):
              try:
                     if (response.status != 200 and response.status != 304):
                            return
                     if (response.encoding is None):
                            return
                     elif (response.encoding != 'utf-8' and response.encoding != 'unicodeescape'):
                            return
                     else:
                            if (response.text != "" or response.text is not None):
                                   
                                   my_json = json.loads(response.text)
                                   conference = my_json['results'][0]['subcategory']
                                   limit = 24
                                   for category,offset in zip(conference,range(5)):
                                          data ={
                                                 'limit': limit,
                                                 'offset': offset,
                                                 'search': {
                                                 'category': conference
                                                 },
                                          }
                                          yield Request(url=self.start_url, headers=DEFAULT_REQUEST_HEADERS, callback=self.parse)
                                          # conference_names.append(category['name'])
                            
              except Exception as e:
                     print(e)


       def parse_paper(self, response):
              

if __name__ == "__main__":
    process  = CrawlerProcess(get_project_settings())
    process.crawl(CrossmindsSpider)
    process.start()