#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = "Ernesto Arbitrio"
SITENAME = "ernestoarbitrio"
SITEURL = "https://ernestoarbitrio.github.io"

PATH = "content"
ARTICLE_PATHS = ["blog"]
ARTICLE_SAVE_AS = "{date:%Y}/{slug}.html"
ARTICLE_URL = "{date:%Y}/{slug}.html"

TIMEZONE = "Europe/Rome"

DEFAULT_LANG = "en"
THEME = "themes/attila"
SITE_LOGO = "images/logo/logoEA.png"
COLOR_SCHEME_CSS = "tomorrow_night.css"
HEADER_COVERS_BY_TAG = [False]
HEADER_COVERS_BY_CATEGORY = [False]
PLUGINS = ["sitemap", "neighbors", "webassets"]
HOME_COLOR = "#e3e3e3"
HOME_COVER = "https://user-images.githubusercontent.com/4196091/119836899-662d0b80-bf02-11eb-8486-f2ea0bac2de1.png"
AUTHORS_BIO = {
    "ernesto arbitrio": {
        "name": "Ernesto Arbitrio",
        "image": "https://avatars.githubusercontent.com/u/4196091?v=4",
        "website": "http://ernestoarbitrio.github.io",
        "linkedin": "ernestoarbitrio/",
        "twitter": "__pamaron__",
        "github": "ernestoarbitrio",
        "location": "Trento",
        "bio": "I'm a senior software backend engineer @ YouGov, python and food passionate!",
        "cover": HOME_COVER
    }
}
# Sitemap
SITEMAP = {
    "format": "xml",
    "priorities": {"articles": 0.5, "indexes": 0.5, "pages": 0.5},
    "changefreqs": {"articles": "monthly", "indexes": "daily", "pages": "monthly"},
}

# Social widget
SOCIAL = (("Twitter", "http://twitter.com/__pamaron__"),)

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None


# Whether to display pages on the menu of the template. Templates may or may not honor
# this setting.
DISPLAY_PAGES_ON_MENU = False
# Whether to display categories on the menu of the template.
DISPLAY_CATEGORIES_ON_MENU = False
# When you don’t specify a category in your post metadata, set this setting to True,
# and organize your articles in subfolders, the subfolder will become the category of
# your post. If set to False, DEFAULT_CATEGORY will be used as a fallback.
USE_FOLDER_AS_CATEGORY = True
# Delete the output directory, and all of its contents, before generating new files.
# This can be useful in preventing older, unnecessary files from persisting in your
# output. However, this is a destructive setting and should be handled with extreme
# care.
DELETE_OUTPUT_DIRECTORY = False
# When creating a short summary of an article, this will be the default
# length (measured in words) of the text created. This only applies if your content
# does not otherwise specify a summary. Setting to None will cause the summary to be a
# copy of the original content.
SUMMARY_MAX_LENGTH = 65
# Leave no orphans
DEFAULT_ORPHANS = 0

# Blogroll
LINKS = (
    ("Pelican", "https://getpelican.com/"),
    ("Python.org", "https://www.python.org/"),
    ("Jinja2", "https://palletsprojects.com/p/jinja/"),
    ("You can modify those links in your config file", "#"),
)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = False

MENUITEMS = (
    ("Home", "/"),
    ("About", "/pages/about.html"),
)

STATIC_PATHS = [
    "images",
    "extras",
]
EXTRA_PATH_METADATA = {
    "extras/favicon.ico": {"path": "favicon.ico"},
}
