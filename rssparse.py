import json
import pathlib
import hashlib
import datetime
import re
import feedparser

RSS = ['http://feeds.bbci.co.uk/news/rss.xml?edition=us',
       'https://www.ncregister.com/feeds/general-news.xml',
       'http://rss.slashdot.org/Slashdot/slashdotMainatom',
       'https://feeds.a.dj.com/rss/WSJcomUSBusiness.xml',
       'https://www.espn.com/espn/rss/oly/news']

def get_rss(url):
    feed = feedparser.parse(url)
    return [{'feed': feed.feed.title,
             'date': datetime.datetime(*x.get('published_parsed', x.get('updated_parsed'))[:6]).isoformat(),
             'title': x.title,
             'summary': re.sub(r'<.*?>', '', x.summary),
             'link': x.link,
             'author': x.get('author'),
             'tags': [z for z in [y.get('term') for y in x.get('tags', [])] +
                      [x.get('wsj_articletype'), x.get('slash_section'), x.get('slash_department')]
                      if z is not None]}
            for x in feed.entries]

def do_all():
    for feed in RSS:
        for entry in get_rss(feed):
            outvers = json.dumps(entry, sort_keys=True)
            outhash = hashlib.sha256(outvers.encode('utf-8')).hexdigest()
            filename = pathlib.Path(outhash + '.json')
            if not filename.exists():
                filename.write_text(outvers)

do_all()
