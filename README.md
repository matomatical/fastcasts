Feed
====

A simple RSS downloader for podcasts, designed to load the files onto my mp3
player.

Features

* configure rss feeds via TOML
* converts all to mp3 while downloading
* converts all to 2x speed while downloading

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

  At the moment it's a hard requirement that the URLs are at depth 3 in the
  TOML---it must always be **category.podcast: rss_url**.
  For example, the following will break the script:

  ```toml
  uncategorized-podcast = "https://example.com/rss"
  too.deeply.nested     = "https://example.com/rss"
  [also-too.deeply]
  nested                = "https://example.com/rss"
  ```

Configure the script:

* Point the `RSS_LIST` variable at your toml file
* Point the `ROOT_PATH` variable at where you want the podcast folders to be
  created.

Usage
-----

Just call the script and wait for it to download/convert all of the episodes.

Development
-----------

TODO:

* test this with non-mp3 files
* make the filename generation more configurable (not always "date-title.mp3")
* make the speedup and formatting configurable? or at least optional? so that
  you can use without ffmpeg if you want
