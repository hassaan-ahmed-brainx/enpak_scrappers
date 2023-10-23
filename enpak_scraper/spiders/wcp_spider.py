# Washington City Paper Spider
# http://washingtoncitypaper.com/

import scrapy
from enpak_scraper.items import NewsItem
from datetime import datetime
from bs4 import BeautifulSoup
from scrapy.utils.project import get_project_settings
settings = get_project_settings()

class WCP_Spider(scrapy.Spider):
  name = "wcp_spider"

  def start_requests(self):
    url = "https://washingtoncitypaper.com/feed/"
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
      print("Author: ", news['author'])

      news['category'] = item.xpath('category/text()').get()
      print("Category: ", news['category'])

      news['state'] = "District of Columbia"
      print("State: ", news['state'])

      news['continent'] = ''

      soup = BeautifulSoup(item.xpath('description/text()').get(), 'html.parser')
      news['description'] = soup.get_text().replace('\n', '').strip()
      print("Description: ", news['description'])

      news['type'] = "Local"
      print("Type: ", news['type'])

      news['source_url'] = item.xpath('link/text()').get() or ''
      print("Source URL: ", news['source_url'])

      news['source_site_logo'] = 'https://criomaticdesigns.com/wp-content/uploads/2022/01/Untitled-design-137.png'
      print("Source Site Logo: ", news['source_site_logo'])

      news['preview_image'] = item.xpath('enclosure/@url').get()
      print("Preview Image: ", news['preview_image'])

      news['source_site_name'] = "Washington City Paper"
      print("Source Site Name: ", news['source_site_name'])

      yield news
