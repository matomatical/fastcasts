import io
import os
import sys
import datetime
import mimetypes

import rtoml as toml
import requests
import podcastparser
import tqdm
import filename_sanitizer as sani

def main():
    # load config
    with open("feeds.toml") as config_file:
        config = toml.load(config_file)

    # process each feed
    for feed_id, feed_data in config.items():
        update_feed(feed_id, **feed_data)

def update_feed(feed_id, url, path):
    print("* updating", feed_id)

    # set up directory
    print(" setting up path", path)
    os.makedirs(path, exist_ok=True)

    # download rss file
    print(" downloading rss file")
    rss_path = os.path.join(path, "rss.xml")
    download_rss(url, rss_path)

    # parse rss file
    print(" parsing rss file")
    rss_feed = parse_rss(url, rss_path)

    # title = rss_feed['title']
    # description = rss_feed['description']
    episodes = rss_feed['episodes']
    print(" found", len(episodes), "episodes")
    for episode in episodes[::-1]:
        try:
            download_episode(episode, path)
        except:
            with open("errors.log", 'a') as f:
                print("ERROR", episode, file=f, flush=True)
                print("ERROR", episode, file=sys.stderr)
                # TODO: handle errors better (a summary at the end of
                # update, for example?)

    print("finished with", feed_id)


def download_rss(url, path):
    print("downloading rss from", url)
    r = requests.get(url)
    r.raise_for_status()
    # (save rss file?)
    with open(path, 'wb') as f:
        f.write(r.content)
    
def parse_rss(url, rss_path):
    with open(rss_path) as f:
        return podcastparser.parse(url, f)

def download_episode(episode, folder_path):
    # episode details
    title = episode['title']
    pubdate = datetime.datetime.fromtimestamp(episode['published'])
    # others: subtitle, description

    # episode file
    file = episode['enclosures'][0]; assert len(episode['enclosures']) == 1
    mimetype = file['mime_type']
    file_url = file['url']
    file_size = file['file_size']

    # compute destination path
    basename = "{yyyymmdd}-{episode_title}{dot_ext}".format(
            episode_title=sani.sanitize_path_fragment(title),
            yyyymmdd=pubdate.strftime("%Y-%m-%d"),
            dot_ext=mimetypes.guess_extension(mimetype),
        )
    path = os.path.join(folder_path, basename)

    # download if doesn't exist yet
    if not os.path.exists(path):
        print(" downloading", basename)
        progress = tqdm.tqdm(
                total=file_size,
                unit="B",
                unit_scale=True,
                unit_divisor=1024,
                leave=False,
                colour="magenta",
                dynamic_ncols=True,
            )
        with requests.get(file_url, stream=True) as r:
            with open(path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=128*1024):
                    progress.update(CHUNK_SIZE)
                    f.write(chunk)
        progress.close()

CHUNK_SIZE = 128*1024


if __name__ == "__main__":
    main()
