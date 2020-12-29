import json

import requests
import time
import random
from utils import download_video

BASE_URL = 'https://crossminds.ai'


def get_conferences():
    r = requests.get('https://api.crossminds.io/content/category/parents/details')
    my_json = json.loads(r.content.decode())
    # with open('test.json', 'r') as f:
    #     my_json = json.load(f)
    conferences = my_json['results'][0]
    conferences_categories = conferences['subcategory']
    conference_names = []
    for category in conferences_categories:
        conference_names.append(category['name'])

    return conference_names


def get_conference_papers(conference, limit, offset):
    data = {
        'limit': limit,
        'offset': offset,
        'search': {
            'category': conference
        },
    }
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.60',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept': '*/*',
        'Content-Type': 'application/json'
    }

    r = requests.post('https://api.crossminds.io/web/content/bycategory', data=json.dumps(data), headers=headers)
    infos = json.loads(r.content.decode())
    # with open('test2.json', 'w') as f:
    #     f.write(r.content.decode())

    return infos


def parser(data):
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


if __name__ == '__main__':
    conferences = get_conferences()
    for conference in conferences:
        limit, offset = 2000, 0
        papers = get_conference_papers(conference, limit=limit, offset=offset)
        for _id, author, title, description, video_source, video_url in parser(papers['results']):
            print(_id, author, description, video_url)
            # download_video(video_source, video_url, title)
        time.sleep(random.uniform(1, 5))
        # if next_request := papers['next_request']:
        #     limit, offset = next_request['limit'], next_request['offset']
        # else:
        #     break
