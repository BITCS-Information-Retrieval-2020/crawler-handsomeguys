import os
import re

from pytube import YouTube


def query_on_dblp(title):
    pass


def query_on_pwc(title):
    pass


def download_video(source, url, target, video_path):
    # target = re.sub(r'\[[\w|\s]*]\s*', '', target)
    # target = re.sub(r'-|\s+', '_', target)
    if source == 'CrossMinds':
        command = f'ffmpeg -i {url} {os.path.join(video_path, target + ".mp4")}'
        os.system(command)
    # elif source == 'YouTube download':
    #     youtube = YouTube(url)
    #     youtube.streams.filter(progressive=True).desc().first().download(output_path=video_path, filename=f'{target}.mp4')
    elif source == 'Vimeo' or source == 'YouTube download' or source == 'YouTube':
        command = f'you-get -s 127.0.0.1:10808 --itag=134 {url} -o {video_path} -O {target}'
        os.system(command)
    else:
        raise RuntimeError(f'Unsupported video source {source}, expected {"CrossMinds", "YouTube download"}')