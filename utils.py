import os


def download_video(source, url, target, video_path):
    if source == 'CrossMinds':
        command = f'ffmpeg -i {url} {os.path.join(video_path, target + ".mp4")}'
        os.system(command)
    elif source == 'Vimeo' or source == 'YouTube download' or source == 'YouTube':
        command = f'you-get -s 127.0.0.1:10808 --itag=134 {url} -o {video_path} -O {target}'
        os.system(command)
    else:
        raise RuntimeError(
            f'Unsupported video source {source}, expected {"CrossMinds", "YouTube download"}'
        )
