#!python3

import io
import os
import sys
import datetime
import mimetypes
import subprocess

import rtoml as toml
import requests
import podcastparser
import tqdm
import filename_sanitizer as sani

CONFIG_PATH = "/Users/matt/.feeds"

def main():
    print("loading config")
    with open(CONFIG_PATH) as config_file:
        podcasts = toml.load(config_file)

    print("processing podcasts")
    for podcast_id, data in podcasts.items():
        os.makedirs(data['path'], exist_ok=True)
        print("updating", podcast_id)
        for episode in download_rss(data['url']):
            download_episode(episode, data['path'])

def download_rss(url):
    print("downloading rss file from", url)
    r = requests.get(url)
    r.raise_for_status()
    rss = podcastparser.parse(url, io.StringIO(r.content.decode()))
    return rss['episodes'][::-1]

def download_episode(episode, folder_path):
    # episode details
    title = episode['title']
    pubdate = datetime.datetime.fromtimestamp(episode['published'])
    # others: subtitle, description

    # episode file
    if episode['enclosures'] == []:
        tqdm.tqdm.write("WARNING: Missing episode file!")
        return
    if len(episode['enclosures']) > 1:
        tqdm.tqdm.write("WARNING: Multiple episode files! (taking first)")
    file = episode['enclosures'][0];
    mimetype = file['mime_type']
    file_url = file['url']
    file_size = file['file_size']

    # compute destination path
    basename = "{yyyymmdd}-{episode_title}.{extension}".format(
            episode_title=sani.sanitize_path_fragment(title),
            yyyymmdd=pubdate.strftime("%Y-%m-%d"),
            extension=".mp3", # guess_extension(mimetype),
        )
    path = os.path.join(folder_path, basename)

    # download if doesn't exist yet
    if not os.path.exists(path):
        print(" downloading", basename)
        progress = tqdm.tqdm(
                total=file_size,
                unit="iB",
                unit_scale=True,
                unit_divisor=1024,
                leave=False,
                colour="magenta",
                dynamic_ncols=True,
            )
        with requests.get(file_url, stream=True) as r:
            ffmpeg_proc = subprocess.Popen(["ffmpeg",
                    # "-i", "pipe:0",             # input from the pipe
                    "-filter:a",                # audio
                    "atempo=2",                 # speed x2 (-vn?)
                    "-vn",                      # remove video stream?
                    "-acodec", "libmp3lame",    # to mp3
                    # "-c:a", "libfdk_aac",       # use apple silicon?
                    path                        # episode name for output?
                ], stdin=subprocess.PIPE)
            for chunk in response.iter_content(chunk_size=1024*128):
                progress.update(1024*128)
                ffmpeg.stdin.write(chunk)
            ffmpeg_proc.stdin.close()
            ffmpeg_proc.wait()
        progress.close()


# # #
# Translating mimetypes
# 
mimetypes.add_type("audio/x-m4a", ".m4a", strict=False)
def guess_extension(mimetype):
    dot_ext = mimetypes.guess_extension(mimetype, strict=False)
    if dot_ext is not None:
        return dot_ext[1:] # without dot
    tqdm.tqdm.write(f"WARNING: unknown mime-type {mimetype!r}! (using mp3)")
    return "mp3"

if __name__ == "__main__":
    main()
