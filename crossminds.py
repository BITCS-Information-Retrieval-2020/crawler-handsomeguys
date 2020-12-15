import requests
import json
from urllib.parse import quote

BASE_URL = 'https://crossminds.ai'

# r = requests.get('https://api.crossminds.io/content/category/parents/details')
# my_json = json.loads(r.content.decode())
with open('test.json', 'r') as f:
    my_json = json.load(f)
conferences = my_json['results'][0]
conferences_categories = conferences['subcategory']
conference_names = []
for category in conferences_categories:
    conference_names.append(category['name'])
# print(conference_names)

conference = conference_names[0]
data = {
    'limit': 24,
    'offset': 0,
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
with open('test2.json', 'w') as f:
    f.write(r.content.decode())
