import os
import re
from pytube import YouTube

VIDEO_PATH = os.path.join('.', 'data', 'videos')


def download_video(source, url, target):
    print(target)
    target = re.sub(r'\[[\w|\s]*]\s*', '', target)
    target = re.sub(r'-|\s+', '_', target)
    print(target)
    exit(0)
    if source == 'CrossMinds':
        command = f'ffmpeg -i {url} {target}'
        os.system(command)
    elif source == 'YouTube download':
        youtube = YouTube(url)
        youtube.streams.filter(progressive=True).desc().first().download(output_path=VIDEO_PATH, filename=f'{target}.mp4')
    else:
        raise RuntimeError(f'Unsupported video source {source}, expected {"CrossMinds", "YouTube download"}')