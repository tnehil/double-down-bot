#!usr/bin/env python3

import feedparser
import re

feeds = ["https://www.minnpost.com/rss.xml",
         "http://www.startribune.com/rss/?sf=1&s=/",
         "http://www.startribune.com/local/index.rss2",
         "http://www.startribune.com/politics/index.rss2",
         "http://www.twincities.com/feed/",
         "http://feeds.mpr.org/MPR_NewsFeatures",
        ]

exp = re.compile(r'[Dd]oubles?[ -][Dd]own')

for feed in feeds:
    f = feedparser.parse(feed)
    for entry in f['entries']:
        if re.search(exp, entry['title']):
            return entry['title'], entry['link']
