import os
import re

from pytube import YouTube

VIDEO_PATH = os.path.join('.', 'data', 'videos')


def query_on_dblp(title):
    pass


def query_on_pwc(title):
    pass


def download_video(source, url, target):
    target = re.sub(r'\[[\w|\s]*]\s*', '', target)
    target = re.sub(r'-|\s+', '_', target)
    if source == 'CrossMinds':
        command = f'ffmpeg -i {url} {target}'
        os.system(command)
    elif source == 'YouTube download':
        youtube = YouTube(url)
        youtube.streams.filter(progressive=True).desc().first().download(output_path=VIDEO_PATH, filename=f'{target}.mp4')
    elif source == 'Vimeo':
        command = f'you-get {url} -o {VIDEO_PATH} -O {target} --debug'
        print(command)
        os.system(command)
    else:
        raise RuntimeError(f'Unsupported video source {source}, expected {"CrossMinds", "YouTube download"}')