# Syracuse Spider
# https://www.syracuse.com/

import scrapy
from enpak_scraper.items import NewsItem
from datetime import datetime
import re
from scrapy.utils.project import get_project_settings
settings = get_project_settings()

class S_Spider(scrapy.Spider):
  name = "s_spider"

  def start_requests(self):
    url = "https://www.syracuse.com/arc/outboundfeeds/rss/?outputType=xml"
    yield scrapy.Request(url=url, callback=self.parse)

  def parse(self, response):
    for item in response.xpath('//rss/channel/item'):
      news = NewsItem()
      print('\n')

      news['title'] = item.xpath('title/text()').get() or ''
      news['title'] = news['title'].strip().replace('\n', '') if news['title'] else news['title']
      print("Title: ", news['title'])

      date = item.xpath('pubDate/text()').get() or ''
      if date:
        date = datetime.strptime(date, "%a, %d %b %Y %H:%M:%S %z")
        news['published_date'] = int(date.timestamp())
      print("Published Date: ", news['published_date'])

      news['author'] = item.xpath('dc:creator/text()', namespaces=settings.get('NS_MAP')).get() or ''
      news['author'] = news['author'].title()
      print("Author: ", news['author'])

      match = re.search(r"/(?:\w+/){0}(\w+)/", item.xpath('link/text()').get() or '')
      news['category'] = match.group(1).capitalize() if match else ''
      print("Category: ", news['category'])

      news['state'] = "New York"
      print("State: ", news['state'])

      news['continent'] = ''

      news['description'] = item.xpath('description/text()').get() or ''
      print("Description: ", news['description'])

      news['type'] = "Local"
      print("Type: ", news['type'])

      news['source_url'] = item.xpath('link/text()').get() or ''
      print("Source URL: ", news['source_url'])

      news['source_site_logo'] = 'https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcQntRnSdZBAAvbYKGG8s4JqpjA_egUHS1YUq66eXO_OUNKTcO-A'
      print("Source Site Logo: ", news['source_site_logo'])

      news['preview_image'] = item.xpath('media:content/@url', namespaces=settings.get('NS_MAP')).get() or ''
      print("Preview Image: ", news['preview_image'])

      news['source_site_name'] = "Syracuse"
      print("Source Site Name: ", news['source_site_name'])

      yield news
