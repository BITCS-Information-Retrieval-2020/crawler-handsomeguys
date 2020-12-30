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
        self.NOTFOUND=404
        # self.delete_one=self.target_coll.delete_one
        # self.delete_many=self.target_coll.delete_many
        self.find=self.target_coll.find
        self.find_one=self.target_coll.find_one

    def construct_checksumdoc(self, doc) -> dict:
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
        return doc4checksum
    
    def insert_one(self, doc) -> int:
        '''
        确保作者以“, ”分隔（英文的逗号和空格）
        返回0（self.SUCESSFUL)表示成功，返回1（self.DUPLICATEKEY）表示是重复的
        '''
        doc4checksum=self.construct_checksumdoc(doc)
        try:
            self.checksum_coll.insert_one(doc4checksum)
        except DuplicateKeyError:
            # 重了
            return self.DUPLICATEKEY
        else:
            self.target_coll.insert_one(doc)
            return self.SUCESSFUL

    def delete_one(self, filter) -> int:
        '''
        返回0（self.SUCESSFUL)表示成功，返回404（self.NOTFOUND）表示是没删除任何东西
        暂时不提供delete_many，可以一个一个删，直到删光。后续根据需要再考虑many
        '''
        doc_del=self.target_coll.find_one(filter)
        # doc4checksum=self.construct_checksumdoc(doc_del)
        # if (self.checksum_coll.delete_one({"_id":doc4checksum["_id"]})).deleted_count>0:
        #     self.target_coll.delete_one(filter)
        #     return self.SUCESSFUL
        # else:
        #     return self.NOTFOUND
        if doc_del is not None:
            doc4checksum=self.construct_checksumdoc(doc_del)
            self.checksum_coll.delete_one({"_id":doc4checksum["_id"]})
            self.target_coll.delete_one(filter)
            return self.SUCESSFUL
        else:
            return self.NOTFOUND

    # def update_one(self, filter, update) -> int:
    #     doc_upd=self.target_coll.find_one(filter)
    #     if doc_upd is not None:
    #         danger=False
    #         for new_value in update.values():
    #             for attr in new_value.keys():
    #                 if attr in ["title", "authors"]:
    #                     danger=True
    #                     break
    #         if danger:
    #             doc4checksum=self.construct_checksumdoc(doc_upd)
                
    #         else:

    # def delete_many(self, query):
    #     return self.target_coll.delete_many(query)

    # def find(self, filter=None):
    #     return