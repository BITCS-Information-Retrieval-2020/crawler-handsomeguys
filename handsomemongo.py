import zlib

import pymongo
from pymongo.errors import DuplicateKeyError

class HandsomeMongo(object):
    def __init__(self, db, target_collection) -> None:
        '''
        理应只创建一个对象，涉及到多线程并发时候调用同一个对象的方法。类似pipelines中的elf.PaperSpiderItem
        封装地比较简单，有接口需要加参数的我再加
        '''
        super().__init__()
        self.checksum_coll=db["checksum"]
        self.target_coll=db[target_collection]
        self.SUCESSFUL=0
        self.DUPLICATEKEY=1
        self.delete_one=self.target_coll.delete_one
        self.delete_many=self.target_coll.delete_many
        self.update=self.target_coll.update
        self.find=self.target_coll.find
        self.find_one=self.target_coll.find_one

    def insert_one(self, doc) -> int:
        '''
        确保作者以“, ”分隔（英文的逗号和空格）
        返回0表示成功，返回1表示是重复的
        '''
        doc_title=doc["title"]
        doc_authors=doc["authors"].split(", ")
        doc_authors_capital=[]
        for author in doc_authors:
            part_name=author.split(' ')
            author_cap=None
            if part_name_len:=len(part_name)>1:
                author_cap=part_name[0][0]+part_name[-1][0]
            elif part_name_len==1:
                author_cap=part_name[0][0]
            else:
                raise NotImplementedError

            doc_authors_capital.append(author_cap)
        doc_authors_capital.insert(0, doc_title)
        doc_checksum=zlib.adler32((" ".join(doc_authors_capital)).encode(encoding="utf-8"))
        doc4checksum={"_id":doc_checksum, "title":doc_title, "authors":doc["authors"]}
        
        try:
            self.checksum_coll.insert_one(doc4checksum)
        except DuplicateKeyError:
            # 重了
            return self.DUPLICATEKEY
        else:
            self.target_coll.insert_one(doc)
            return self.SUCESSFUL

    # def delete_one(self, query):
    #     return self.target_coll.delete_one(query)

    # def delete_many(self, query):
    #     return self.target_coll.delete_many(query)

    # def find(self, filter=None):
    #     return