# Democrat & Chronicle Spider
# https://www.democratandchronicle.com/

import scrapy
from enpak_scraper.items import NewsItem
from datetime import datetime
import re
from bs4 import BeautifulSoup
from scrapy.utils.project import get_project_settings
settings = get_project_settings()

class DAC_Spider(scrapy.Spider):
  name = "dac_spider"

  def start_requests(self):
    url = "https://rssfeeds.democratandchronicle.com/Democratandchronicle/BreakingNewsAndTopStories"
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

      match = re.search(r"/(?:\w+/){1}(\w+)/", item.xpath('feedburner:origLink/text()', namespaces=settings.get('NS_MAP')).get() or '')
      news['category'] = match.group(1).capitalize() if match else ''
      print("Category: ", news['category'])

      news['state'] = "New York"
      print("State: ", news['state'])

      news['continent'] = ''

      description = item.xpath('description/text()').get() or ''
      soup = BeautifulSoup(description, 'html.parser')
      news['description'] = soup.get_text().replace('\n', '').strip()
      print("Description: ", news['description'])

      news['type'] = "Local"
      print("Type: ", news['type'])

      news['source_url'] = item.xpath('link/text()').get() or ''
      print("Source URL: ", news['source_url'])

      news['source_site_logo'] = 'https://thechildrensagenda.org/wp-content/uploads/2019/04/d_and_c_logo_new.jpg'
      print("Source Site Logo: ", news['source_site_logo'])

      news['preview_image'] = item.xpath('enclosure/@url').get() or ''
      print("Preview Image: ", news['preview_image'])

      news['source_site_name'] = "Democrat & Chronicle"
      print("Source Site Name: ", news['source_site_name'])

      yield news
