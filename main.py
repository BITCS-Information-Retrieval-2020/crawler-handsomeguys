import os
import re
from pymongo import MongoClient
from utils import download_video
from multiprocessing import Pool

VIDEO_PATH = os.path.join('.', 'data', 'videos')

if __name__ == '__main__':
    # 运行 crossminds 爬虫
    command = 'cd Crossminds && scrapy crawl crossminds $$ cd ..'
    os.system(command)

    # 以下代码用于视频的下载
    # 连接到数据库
    client = MongoClient('mongodb://handsomeguys:12138@47.103.222.126:27017/crawler')
    my_db = client['crawler']
    my_col = my_db['papers']

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
