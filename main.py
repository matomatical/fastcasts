import io
import os
import pprint
import datetime
import mimetypes
import subprocess

import tomli as tomllib # TODO replace with tomllib in python 3.11+
import tqdm
import requests
import podcastparser
import filename_sanitizer as sani


RSS_LIST  = "./feeds.toml"
ROOT_PATH = "./downloads/"


def main():
    # load list of files
    with open(RSS_LIST, 'rb') as rss_list_path:
        feeds = tomllib.load(rss_list_path)
    # walk list of files
    for folder, podcasts in feeds.items():
        for podcast, rss_url in podcasts.items():
            path = os.path.join(ROOT_PATH, folder, podcast)
            print("PODCAST", path)
            os.makedirs(path, exist_ok=True)
            # download and parse rss
            rss_stream = io.BytesIO(requests.get(rss_url, stream=True).content)
            rss = podcastparser.parse(rss_url, rss_stream)
            # loop through episodes
            episodes = rss['episodes']
            for episode in episodes[::-1]:
                # derive path to episode
                title = "{:%Y%m%d}-{}.mp3".format(
                    datetime.datetime.fromtimestamp(episode['published']),
                    sani.sanitize_path_fragment(episode['title']),
                )
                episode_path = os.path.join(path, title)
                if os.path.exists(episode_path):
                    print("EPISODE", title, "(skip)")
                    continue
                else:
                    print("EPISODE", title)

                # find the episode url
                files = episode['enclosures']
                if len(files) == 0:
                    print("WARNING: Missing file! (skipping)")
                    continue
                if len(files) > 1:
                    print("WARNING: Multiple files! (using first only)")
                episode_url = files[0]['url']

                # download from episode url to episode path
                download_and_format(episode_url, episode_path)


def download_and_format(url, path):
    r = requests.get(url, stream=True)
    filesize = int(r.headers.get('Content-Length'))
    mimetype = r.headers.get('Content-Type')
    extension = guess_extension(mimetype)

    ffmpeg = subprocess.Popen(
        [
            'ffmpeg',
            '-i', 'pipe:',              # read from stdin
            '-filter:a', 'atempo=2.0',  # audio speed x2
            '-vn',                      # remove video?
            "-acodec", "libmp3lame",    # to mp3?
            '-f', extension,
            path,
        ],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE, # captures, but I do nothing with it
        stderr=subprocess.PIPE, # captures, but I do nothing with it
    )
    
    progress = tqdm.tqdm(
        total=filesize,
        unit="iB",
        unit_scale=True,
        unit_divisor=1024,
        leave=False,
        colour="magenta",
        dynamic_ncols=True,
    )

    for chunk in r.iter_content(chunk_size=1024*128):
        progress.update(len(chunk))
        ffmpeg.stdin.write(chunk)
    
    ffmpeg.stdin.close()
    ffmpeg.wait()
    progress.close()
    r.close()


# mimetypes
mimetypes.add_type("audio/x-m4a", ".m4a", strict=False)
def guess_extension(mimetype):
    dot_ext = mimetypes.guess_extension(mimetype, strict=False)
    if dot_ext is not None:
        return dot_ext[1:] # without dot
    tqdm.tqdm.write(f"WARNING: unknown mime-type {mimetype!r}! (using mp3)")
    return "mp3"


if __name__ == "__main__":
    main()
