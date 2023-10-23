# Alabama Spider
# http://al.com/

import scrapy
from enpak_scraper.items import NewsItem
from datetime import datetime
from bs4 import BeautifulSoup
import re
from scrapy.utils.project import get_project_settings
settings = get_project_settings()

class AL_Spider(scrapy.Spider):
  name = "al_spider"

  def start_requests(self):
    url = "https://www.al.com/arc/outboundfeeds/rss/?outputType=xml"
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

      news['state'] = "Alabama"
      print("State: ", news['state'])

      news['continent'] = ''

      soup = BeautifulSoup(item.xpath('content:encoded/text()', namespaces=settings.get('NS_MAP')).get(), 'html.parser')
      news['description'] = soup.get_text().strip()
      print("Description: ", news['description'])

      news['type'] = "Local"
      print("Type: ", news['type'])

      news['source_url'] = item.xpath('link/text()').get() or ''
      print("Source URL: ", news['source_url'])

      news['source_site_logo'] = 'https://is1-ssl.mzstatic.com/image/thumb/Purple126/v4/2e/0b/8b/2e0b8ba7-d204-651f-f141-c58680a16e3b/AppIcon-0-1x_U007emarketing-0-10-0-85-220.png/1200x630wa.png'
      print("Source Site Logo: ", news['source_site_logo'])

      image = soup.find('img')
      news['preview_image'] = image.get('src') if image else ''
      print("Preview Image: ", news['preview_image'])

      news['source_site_name'] = "Alabama"
      print("Source Site Name: ", news['source_site_name'])

      yield news
