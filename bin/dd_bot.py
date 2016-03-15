#!usr/bin/env python3

import feedparser
import re
import os
from slacker import Slacker

slack_token = os.environ['DD_BOT_TOKEN']
slack_channel = "#socialmedia" #update to use env variable probably

slack = Slacker(slack_token)

feeds = [("MINNPOST", "https://www.minnpost.com/rss.xml"),
         ("THE STAR TRIBUNE", "http://www.startribune.com/rss/?sf=1&s=/"),
         ("THE STAR TRIBUNE", "http://www.startribune.com/local/index.rss2"),
         ("THE STAR TRIBUNE", "http://www.startribune.com/politics/index.rss2"),
         ("THE PIONEER PRESS","http://www.twincities.com/feed/"),
         ("MPR","http://feeds.mpr.org/MPR_NewsFeatures"),
        ]

exp = re.compile(r'[Dd]oubl.*[ -][Dd]own')

for feed in feeds:
    title, url = feed
    f = feedparser.parse(url)
    for entry in f['entries']:
        if re.search(exp, entry['title']):
            slack.chat.post_message(slack_channel, "%s IS DOUBLING DOWN: %s" % (title, entry['link'])
