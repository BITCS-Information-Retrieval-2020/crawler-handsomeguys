import os
import re


def download_video(source, target):
    target = re.sub(r'-|\s+', '_', target)
    command = f'ffmpeg -i {source} {target}'
    os.system(command)
