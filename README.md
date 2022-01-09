Feed
====

A simple RSS downloader for podcasts, inspired by castget.

Requirements
------------

Install dependencies:

* `pip install rtoml`
  a fast rust-based toml parser for reading config files
* some downloader... apparently libcurl is faster than `requests` but I can't
  get it to work yet! So `pip install requests`
* `pip install podcastparser`

Configuration
-------------

In a home-directory file `~/.config/feed.conf`:

```
# some id for each feed
[some_id]
url       = "some.example.com/rss"
path      = "Users/matt/podcasts/{id}"
filename  = "{id}-{date}-{title}.{ext}"

# more feeds below
```

This configuration format from castget is really neat and I think it's worth
sharing with my other project 'mess'. Also, is this just TOML? Castget uses
a format with no strings so it's a bit different. Also, what kind of filename
and path fields can be automatically populated? How about:

* `{id}` for the id of the podcast (in this case `some_id`).
* `{date}` for the date of the episode (in the format `YYYY-MM-DD` for
  sorting).
* `{title}` for the title of the episode.
* `{index}` for the index of the episode within the RSS feed (this is not
  necessarily the same as the episode number if the podcast uses those).
* `{filename}` for the filename of the podcast (not including the extension).
* `{ext}` for the filename extension from the filename of the podcast.
  Actually, maybe this should be automatically added, because I can't see a
  reason why not to keep the filename **all cases.**

These are Python format-strings so you can do `{` as `{{` etc.

Usage
-----

From anywhere, run a simple command like `feed` and all podcasts will be
updated.
