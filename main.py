import io
import os
import datetime
import mimetypes

import tomli as tomllib # TODO replace with tomllib in python 3.11+
import tqdm
import requests
import podcastparser
import filename_sanitizer as sani


RSS_LIST  = "./feeds.toml"
ROOT_PATH = "./downloads/"


def main():
    with open(RSS_LIST, 'rb') as rss_list_path:
        feeds = tomllib.load(rss_list_path)
    for folder, podcasts in feeds.items():
        for podcast, rss_url in podcasts.items():
            print("PODCAST", podcast)
            path = os.path.join(ROOT_PATH, folder, podcast)
            update_feed(rss_url, path)


def update_feed(rss_url, path):
    # setup folder
    os.makedirs(path, exist_ok=True)
    # download and parse rss
    rss_stream = io.BytesIO(requests.get(rss_url).content)
    rss = podcastparser.parse(rss_url, rss_stream)
    # download all episodes
    episodes = rss['episodes']
    for episode in episodes[::-1]:
        download_episode(episode, path)


def download_episode(episode, folder_path):
    title   = episode['title']
    pubdate = datetime.datetime.fromtimestamp(episode['published'])

    # episode file
    if episode['enclosures'] == []:
        print("WARNING: Missing episode file!")
        return
    if len(episode['enclosures']) > 1:
        print("WARNING: Multiple episode files! (taking first)")
    file = episode['enclosures'][0];
    mimetype = file['mime_type']
    file_url = file['url']
    file_size = file['file_size']

    # compute destination path
    basename = "{yyyymmdd}-{episode_title}.{extension}".format(
            episode_title=sani.sanitize_path_fragment(title),
            yyyymmdd=pubdate.strftime("%Y-%m-%d"),
            extension=guess_extension(mimetype),
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
            with open(path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024*128):
                    progress.update(1024*128)
                    f.write(chunk)
        progress.close()


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
