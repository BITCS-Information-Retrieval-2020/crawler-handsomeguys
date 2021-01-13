"""
README

Title2content:实现输入论文title，返回paperswithcode上论文相关信息的类
方法：
title2prepage():输入title，返回搜索结果页面的url
prepage2page():输入搜索结果页面的url。返回每篇相关论文的主页url
page2content():输入论文主页的url，得到论文的所有相关信息

调用方法：
title2content = Title2content()
results = title2content.search(title)  # title为传入的论文标题参数，类型为str

返回结果：
list of dict，每篇论文对应一个字典
Example:
    [
        {
            'pdfUrl': 'https://arxiv.org/pdf/2101.02046v2.pdf',
            'year': '2021',
            'publicationOrg': '',
            'authors': ['junyi-li', 'tianyi-tang', 'gaole-he',...],
            'abstract': 'We release an open library, called TextBox...',
            'codeUrl': 'https://github.com/RUCAIBox/TextBox',
            'pdfPath': '',
            'publicationUrl': '',
            'videoUrl': '',
            'videoPath': '',
        },
        ...
    ]
"""
import requests
from lxml import etree
import urllib.parse
import re


class Title2content(object):
    """
    class that controls the title2content search process
    """
    def __init__(self):

        self.baseurl = 'https://www.paperswithcode.com/search?q_meta=&q='
        self.header = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                                     "(KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66",
                       'Referer': "https://www.paperswithcode.com/search?q_meta=&q=Voice+Separation+with+an+Unknown+"
                                  "Number+of+Multiple+Speakers"}
        self.pages_xpath = '/html/body/div[3]/div/div[2]/div/div[2]/div/div[2]/div[2]/a[1]/@href'
        self.page_pdfs_xpath = '/html/body/div[13]/div/div[2]/div/div/a/@href'  # pdf abstract icml2020
        self.page_codes_xpath = '//*[@id="id_paper_implementations_collapsed"]/div/div[1]/div/a/@href'
        self.page_text_xpath = '/html/body/div[13]/div/div[2]/div/div/p/text()'
        self.arxiv_header = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                           "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
                             'Referer': "https://arxiv.org/"}
        self.author_xpath = '/html/body/div[13]/div/div[1]/div/div/div/p/span/a'
        self.comments_authors_xpath = '/html/body/div[13]/div/div[1]/div/div/div/p/span/a/@href'
        self.subtext_xpath = '/html/body/div[13]/div/div[1]/div/div/div/p/span/text()'

    def title2prepage(self, title):
        """
        title到前导页，前导页中的paper和code都链向true page
        """
        title = urllib.parse.quote(title)
        tail = '+'.join(title.split())
        url = self.baseurl + tail
        return url    # prepage url

    def prepage2page(self, preurl):
        """
        prepage中有多个paper和code，即返回多个page的url
        """
        r = requests.get(preurl, headers=self.header)
        selector = etree.HTML(r.text.encode('utf-8'))

        pages_url = selector.xpath(self.pages_xpath)  # 可能有多篇论文
        for i in range(len(pages_url)):
            pages_url[i] = 'https://www.paperswithcode.com' + pages_url[i]
        return pages_url  # 在prepage页面中得到每篇论文的主页，返回值为论文主页url列表

    def page2content(self, pages_url):
        """
        由论文主页的url得到pdf等内容的url
        """
        results = []
        for url in pages_url:  # 对每篇论文主页的url
            t = dict()
            r = requests.get(url, headers=self.header)
            selector = etree.HTML(r.text.encode('utf-8'))

            pdfs_url = selector.xpath(self.page_pdfs_xpath)
            codes_url = selector.xpath(self.page_codes_xpath)
            t['pdfUrl'] = pdfs_url[0]
            info = selector.xpath(self.comments_authors_xpath)
            judge = info[0].split('/')[-1].split('-')[1]
            if re.match(r"\d{4}", judge) is None:  # 第一个位置不是出版方和年份，仅作者
                authors_list = info
                subtext = selector.xpath(self.subtext_xpath)[0]  # 从subtitletext中获得年份信息
                t["year"] = subtext.split()[-1]
                t["publicationOrg"] = ''
            else:  # 第一个位置是出版方和年份
                authors_list = info[1:]
                t["year"] = info[0].split('/')[-1].split('-')[1]
                t["publicationOrg"] = info[0].split('/')[-1].split('-')[0].upper()
            authors_result = []
            for i in authors_list:
                authors_result.append(i.split('/')[-1])
            t["authors"] = authors_result
            t["abstract"] = ''.join(selector.xpath(self.page_text_xpath)).replace('\n', '').strip()
            t["codeUrl"] = codes_url[0]
            t["pdfPath"] = ''
            t["publicationUrl"] = ''
            t["videoUrl"] = ''
            t["videoPath"] = ''
            results.append(t)
        return results

    def search(self, title: str) -> list:
        preurl = self.title2prepage(title)
        pages_url = self.prepage2page(preurl)
        results = self.page2content(pages_url)
        return results
