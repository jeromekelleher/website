#!/usr/bin/env python3
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

DISPLAY_PAGES_ON_MENU = True
DISPLAY_CATEGORIES_ON_SUBMENU = False

AUTHOR = u'Jerome Kelleher'
SITENAME = u"Python - Algorithms - Bioinformatics"
SITEURL = 'http://jeromekelleher.net'

THEME = "pelican-blueidea/"

TIMEZONE = 'Europe/London'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# # Blogroll
# LINKS =  (('Pelican', 'http://getpelican.com/'),
#           ('Python.org', 'http://python.org/'),
#           ('WTCHG', 'http://www.well.ox.ac.uk/'),)


# Social widget
SOCIAL = (('twitter', 'https://twitter.com/jeromekelleher'),
          ('github', 'https://github.com/jeromekelleher'),)

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

# Where to look for plugins
PLUGIN_PATHS = ['../pelican-plugins']
# Which plugins to enable
PLUGINS = []
