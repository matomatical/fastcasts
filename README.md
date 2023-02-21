Feed
====

A simple RSS downloader for podcasts, designed to load the files onto my mp3
player.

Features

* configure rss feeds via TOML
* converts all formats to mp3 while downloading (this is what fits on my mp3
  player)
* converts all formats to 2x speed while downloading (the player has limited
  speed control)

Installation
------------

Install Python dependencies (`pip install` the following)

* `tomli` a minimal TOML parser (TODO: migrate to python 3.11 `tomllib`)
* `tqdm` for pretty CLI progress bars
* `requests` URL downloader
* `podcastparser` to parse RSS feeds
* `filename_sanitizer` to convert titles to permissible path fragments

Install other dependencies (see your package manager):

* `ffmpeg` to convert to mp3 and speed up the files

Optional:

* Make the script executable and add it to your path so you can sync podcasts
  from anywhere.

Configuration
-------------

List RSS feeds:

* Put somewhere a toml file containing a list of categories and within the
  categories various podcasts:

  ```toml
  [economics]

  econtalk              = "https://feeds.simplecast.com/wgl4xEgL"

  [philosophy]

  philosopher-and-news  = "https://feeds.buzzsprout.com/1577503.rss"
  
  [misc]

  not-related           = "https://notrelated.xyz/rss"
  ezra-klein            = "https://feeds.simplecast.com/82FI35Px"
  ```

  In the example all the URLs are at depth 3 (there is a category key and a
  podcast title key and then the URL), but this is not a hard requirement.
  The script will create folders mirroring the TOML table (dictionary)
  structure and I guess it can go arbitrarily deep.

* It's just a TOML file so you can for example comment out podcasts you don't
  want to sync every single time (for example if they are no lonher expected
  to be updated or you're just not listening to them at the moment)

My example is included in the repo.

Configure the script:

* Point the `RSS_LIST` variable at your toml file
* Point the `ROOT_PATH` variable at where you want the podcast folders to be
  created.

Usage
-----

Just call the script and wait for it to download/convert all of the episodes.

Let me know if any issues.

Development
-----------

TODO:

* add better error handling so that if something goes wrong with (1)
  downloading or (2) ffmpeg or (3) OS I can tell which, and have useful
  information such as the ffmpeg error, the url, the path, etc.

* make the filename generation more configurable (not always "date-title.mp3")

* make the speedup and mp3-formatting configurable? or at least optional? so
  that you can use without ffmpeg if you want a simple podcast downloader
