# -*- coding: utf-8 -*-
import json
import os

import scrapy
from Crossminds.items import CrossmindsItem, PDFItem
from Crossminds.settings import DEFAULT_REQUEST_HEADERS
from scrapy.crawler import CrawlerProcess
from scrapy.http import Request
from scrapy.utils.project import get_project_settings
from tqdm import tqdm
import re


def get_conferences(data):
    # 从返回的 json 字符串中获得 json 数据
    my_json = json.loads(data)

    conferences = my_json['results'][0]
    conferences_categories = conferences['subcategory']
    conference_names = []
    for category in conferences_categories:
        conference_names.append(category['name'])

    return conference_names


def parse_paper(data):
    for info in data:
        _id = info['_id']
        author = {
            'name': info['author']['name'],
            'email': info['author']['email']
        }
        title = info['title']
        description = info['description']
        video_source = info['source']
        video_url = info['video_url']

        yield _id, author, title, description, video_source, video_url


class CrossmindsSpider(scrapy.Spider):
    name = 'Crossminds'
    start_url = 'https://api.crossminds.io/content/category/parents/details'
    second_url = 'https://api.crossminds.io/web/content/bycategory'

    def start_requests(self):
        yield Request(url=self.start_url, headers=DEFAULT_REQUEST_HEADERS, callback=self.parse)

    def parse(self, response, **kwargs):
        # 获取会议列表
        conferences = get_conferences(response.text)
        # 获取每一个会议
        for conference in tqdm(conferences):
            # time.sleep(random.uniform(1, 5))
            body = json.dumps({'limit': 5000, 'offset': 0, 'search': {'category': conference}})
            yield Request(url=self.second_url, method='post', headers=DEFAULT_REQUEST_HEADERS, body=body,
                          callback=lambda res, con=conference: self.parse_detail(res, con))

    def parse_detail(self, response, conference):
        info = CrossmindsItem()
        pdfs = PDFItem()
        org, year = conference.split(' ')
        papers = json.loads(response.text)
        for _id, author, title, description, video_source, video_url in parse_paper(papers['results']):
            info['id'] = _id
            info['title'] = title
            info['authors'] = author['name']
            info['publicationOrg'] = org
            info['year'] = year
            info['description'] = description
            info['videoUrl'] = video_url
            info['source'] = video_source
            yield info

            url_list = []
            pattern = r'(http|https)://[\w\./-]+'
            url = re.search(pattern, description)
            while url:
                url_list.append(url.group())
                start, end = url.span()
                description = description[:start] + description[end + 1:]
                url = re.search(pattern, description)

            pdfs['file_names'] = title
            for url in url_list:
                if 'arxiv.org/abs' in url:
                    url = url.replace('abs', 'pdf')
                    url += '.pdf'
                    pdfs['file_urls'] = url
                    yield pdfs
                elif '.pdf' in url:
                    pdfs['file_urls'] = url
                    yield pdfs


if __name__ == "__main__":
    process = CrawlerProcess(get_project_settings())
    process.crawl(CrossmindsSpider)
    process.start()
