import os
import re
from pymongo import MongoClient
from utils import download_video
from multiprocessing import Pool
from handsomemongo import HandsomeMongo
from pymongo.collection import Collection

VIDEO_PATH = os.path.join('.', 'data', 'videos')
KEYS = ['_id', 'title', 'authors', 'abstract', 'publicationOrg', 'year', 'pdfUrl', 'pdfPath', 'publicationUrl', 'codeUrl', 'videoUrl', 'videoPath']


def format_path(path):
    path = re.sub(r'\.{2,}', '.', path)
    path = re.sub(r'\\', '/', path)
    return path


def format_authors(authors):
    if isinstance(authors, list):
        f_authors = authors[0]
        for author in authors[1:]:
            f_authors += ', ' + author
        return f_authors
    return authors


def merge(source: Collection, target: Collection, update_pdf=False, update_code=False):
    queries = source.find()
    for query in queries:
        new_data = {}
        for key in KEYS:
            if key not in query:
                new_data[key] = ''
            elif key == '_id':
                cur_count = target.estimated_document_count()
                new_id = cur_count + 1
                new_data['_id'] = new_id
            else:
                new_data[key] = query[key]

        new_data['authors'] = format_authors(new_data['authors'])
        new_data['pdfPath'] = format_path(new_data['pdfPath'])
        new_data['video_path'] = format_path(new_data['video_path'])

        status, dup_doc = handsomemongo.insert_one(new_data)
        if status == 1:
            if update_pdf:
                pdf_url = new_data['pdfUrl']
                if pdf_url != '':
                    handsomemongo.update_one({'_id': dup_doc['_id']}, {'$set': {'pdfUrl': pdf_url}})
            if update_code:
                code_url = new_data['codeUrl']
                if code_url != '':
                    handsomemongo.update_one({'_id': dup_doc['_id']}, {'$set': {'codeUrl': code_url}})


if __name__ == '__main__':
    # 运行 crossminds 爬虫
    command = 'cd Crossminds && scrapy crawl crossminds && cd ..'
    os.system(command)

    # 运行 papers with code
    command = 'cd Paperwithcode && scrapy crawl paperswithcode && cd ..'
    os.system(command)

    # 运行 dblp
    command = 'cd cd Dblp && scrapy crawl Dblp && cd ..'
    os.system(command)

    # 连接到数据库
    client = MongoClient('mongodb://handsomeguys:12138@47.103.222.126:27017/crawler')
    my_db = client['crawler']
    my_col = my_db['papers']

    handsomemongo = HandsomeMongo(db=my_db, target_collection='papers')
    # 转移 crossminds 数据
    merge(source=my_db['test'], target=my_db['papers'])
    # 转移 papers with code 数据
    merge(source=my_db['paperswithcode'], target=my_db['papers'], update_pdf=True, update_code=True)
    # 转移 dblp 数据
    merge(source=my_db['dblp'], target=my_db['papers'])

    # 查询需要下载视频的数据
    queries = my_col.find({}, {'title': 1, 'videoUrl': 1, 'source': 1})
    # 创建进程池
    pool = Pool(processes=4)
    for query in queries:
        _id, title, videoUrl, source = query['_id'], query['title'], query['videoUrl'], query['source']
        # 去除文件名中的非法字符
        video_name = re.sub(r'[^A-Za-z0-9_]', ' ', title)
        video_name = video_name.strip()
        video_name = re.sub(r'\s+', '_', video_name)
        save_path = os.path.join(VIDEO_PATH, video_name + '.mp4')
        # 若该视频不存在则调用 download_video() 函数下载
        if not os.path.exists(save_path):
            my_col.update_one({"_id": _id}, {"$set": {"videoPath": save_path}})
            pool.apply_async(download_video, args=[source, videoUrl, video_name, VIDEO_PATH])

    pool.close()
    pool.join()
