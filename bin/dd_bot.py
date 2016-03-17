#!usr/bin/env python3

import feedparser
import re
import os
import json
import redis
from slacker import Slacker

slack_token = os.environ['DD_BOT_TOKEN']
slack = Slacker(slack_token)

redis_url = os.environ['DD_REDIS_URL']
cache = redis.StrictRedis.from_url(redis_url)

fp = open('config.json', 'r')
config = json.load(fp)
fp.close()

slack_channel = config['slack_channel']
feeds = config['feeds']


exp = re.compile(r'[Dd]oubl.*\b[Dd]own')

for feed in feeds:
    outlet, url = feed['outlet'], feed['feed_url']
    f = feedparser.parse(url)
    dds = 0
    for entry in f['entries']:
        if re.search(exp, entry['title']) and cache.get(entry['link']) == None:
            slack.chat.post_message(slack_channel,
                                    "%s IS DOUBLING DOWN: %s" % (outlet, entry['link']),
                                    as_user=True)
            cache.setex(entry['link'], 60*60*24*7, '')
            dds +=1

print("Found %s double-downs" % dds)
