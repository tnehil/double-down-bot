#!usr/bin/env python3

import feedparser
import re
import os
import json
from slacker import Slacker

slack_token = os.environ['DD_BOT_TOKEN']
slack_channel = "#socialmedia" #update to use env variable probably
slack = Slacker(slack_token)

redis_url = os.environ['DD_REDIS_URL']
cache = redis.StrictRedis.from_url(redis_url)

fp = open('../feeds.json', 'r')
feeds = json.load(fp)['feeds']
fp.close()

exp = re.compile(r'[Dd]oubl.*\b[Dd]own')

for feed in feeds:
    outlet, url = feed['outlet'], feed['feed_url']
    f = feedparser.parse(url)
    for entry in f['entries']:
        if re.search(exp, entry['title']) and not cache.get(entry['link']):
            slack.chat.post_message(slack_channel,
                                    "%s IS DOUBLING DOWN: %s" % (outlet, entry['link']),
                                    as_user=True)
            cache.setex(entry['link'], 60*60*24*7, '')
