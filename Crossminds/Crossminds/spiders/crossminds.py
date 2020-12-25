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
       second_url = 'https://api.crossminds.io/web/content/bycategory'

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
                                                 'category': category['name']
                                                 },
                                          }
                                          final_data = json.dumps(data)
                                          yield Request(url=self.second_url,headers=DEFAULT_REQUEST_HEADERS,method='POST',body=final_data,callback=self.parse_paper)
                                          # yield FormRequest(url=self.second_url, headers=DEFAULT_REQUEST_HEADERS, callback=self.parse_paper,formdata=final_data)
              except Exception as e:
                     print(e)


       def parse_paper(self, response):
              info = CrossmindsItem()
              try:
                     if (response.status != 200 and response.status != 304):
                            return
                     if (response.encoding is None):
                            return
                     elif (response.encoding != 'utf-8' and response.encoding != 'unicodeescape'and response.encoding != 'cp1252'):
                            return
                     else:
                           if (response.text != "" or response.text is not None): 
                                   my_json = json.loads(response.text)
                                   results = my_json['results']
                                   for result in results:
                                          info['title'] = result['title']
                                          info['video_url'] = result['video_url']
                                          info['author_email'] = result['author']['email']
                                          # info['time'] = result['updated_at']
                                          info['author'] = result['author']['name']
                                          info['author_photo'] = result['author']['photoURL']
                                          info['description'] = result['description']
                                          info['author_id'] = result['author_id']
                                          yield info
              except Exception as e:
                     print(e)

if __name__ == "__main__":
    process  = CrawlerProcess(get_project_settings())
    process.crawl(CrossmindsSpider)
    process.start()