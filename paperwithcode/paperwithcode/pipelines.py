# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
from paperwithcode.items import PaperwithcodeItem
from paperwithcode.settings import FILE_STORED_PATH
import os


class PaperwithcodePipeline(object):
    def open_spider(self, spider):
        self.client = pymongo.MongoClient('mongodb://47.103.222.126:27017')
        db = self.client['crawler']
        db.authenticate('handsomeguys', '12138')
        self.collection = db['paperswithcode']

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, PaperwithcodeItem):
            self.insert_item(item)
        if item['pdfContent'] is not None:
            self.save_pdf(title=item['title'], content=item['pdfContent'])
        return item

    def insert_item(self, item):
        insert_data = {
            "title": item['title'],
            "authors": item['authors'],
            "abstract": item['abstract'],
            "publicationOrg": item['publicationOrg'],
            "year": item['year'],
            "pdfUrl": item['pdfUrl'],
            "publicationUrl": item['publicationUrl'],
            "codeUrl": item['codeUrl'],
        }
        query = list(
            self.collection.find({}, {
                "_id": 1
            }).sort('_id', -1).limit(1))
        insert_data['_id'] = 1 if len(query) == 0 else query[0]['_id'] + 1
        self.collection.insert_one(insert_data)

    def save_pdf(self, title, content):
        path = os.path.join(FILE_STORED_PATH, title + '.pdf')
        with open(path, 'wb') as f:
            f.write(content)
