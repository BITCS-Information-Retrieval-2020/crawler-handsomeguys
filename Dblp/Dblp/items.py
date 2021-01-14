# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DblpItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    authors = scrapy.Field()
    abstract = scrapy.Field()
    publicationOrg = scrapy.Field()
    year = scrapy.Field()
    pdfUrl = scrapy.Field()
    pdfPath = scrapy.Field()
    publicationUrl = scrapy.Field()
    codeUrl = scrapy.Field()
    videoUrl = scrapy.Field()
    videoPath = scrapy.Field()
    files = scrapy.Field()  # 文件下载完成后会往里面写相关的信息
    pass
    # helper
    # fileName = scrapy.Field()
    # pdfDownloadUrl = scrapy.Field()


class PDFItem(scrapy.Item):
    file_urls = scrapy.Field()  # 指定文件下载的连接
    files = scrapy.Field()  # 文件下载完成后会往里面写相关的信息
    file_names = scrapy.Field()
