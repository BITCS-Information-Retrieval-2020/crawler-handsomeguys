# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PaperwithcodeItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    authors = scrapy.Field()
    abstract = scrapy.Field()
    publicationOrg = scrapy.Field()
    year = scrapy.Field()
    pdfUrl = scrapy.Field()
    publicationUrl = scrapy.Field()
    codeUrl = scrapy.Field()
    pdfContent = scrapy.Field()
