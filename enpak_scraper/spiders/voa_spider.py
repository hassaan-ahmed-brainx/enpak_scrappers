# Voice Of America Spider
# https://www.voanews.com/

import scrapy
from enpak_scraper.items import NewsItem
from datetime import datetime
import re
from scrapy.utils.project import get_project_settings
settings = get_project_settings()

class VOA_Spider(scrapy.Spider):
  name = "voa_spider"

  def start_requests(self):
    urls = ["https://www.voanews.com/api/zqbomekvi_", "https://www.voanews.com/api/zobo_egviy", "https://www.voanews.com/api/zjboveytit", "https://www.voanews.com/api/z-botevtiq"]
    yield scrapy.Request(url=urls[0], callback=self.parse, cb_kwargs={'continent': "Americas"})
    yield scrapy.Request(url=urls[1], callback=self.parse, cb_kwargs={'continent': "Asia"})
    yield scrapy.Request(url=urls[2], callback=self.parse, cb_kwargs={'continent': "Europe"})
    yield scrapy.Request(url=urls[3], callback=self.parse, cb_kwargs={'continent': "Africa"})

  def parse(self, response, continent):
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

      author = item.xpath('author/text()').get() or ''
      match = re.search(r"\((.*?)\)", author)
      news['author'] = match.group(1) if match else ''
      print("Author: ", news['author'])

      news['category'] = item.xpath('category/text()').get()
      print("Category: ", news['category'])

      news['state'] = ''

      news['continent'] = continent
      print("Continent: ", news['continent'])

      description = item.xpath('description/text()').get() or ''
      if description:
        lines = description.split('\n')
        news['description'] = lines[:5]
        news['description'] = ''.join(news['description'])
      print("Description: ", news['description'])

      news['type'] = "International"
      print("Type: ", news['type'])

      news['source_url'] = item.xpath('link/text()').get() or ''
      print("Source URL: ", news['source_url'])

      news['source_site_logo'] = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSXhGq5rv_ViluZ6LF4dPx9xqQXCB9l1TLyFvmv_LlCs_mQHxChdRVh52BsGXMGHVsSPCs&usqp=CAU'
      print("Source Site Logo: ", news['source_site_logo'])

      news['preview_image'] = item.xpath('enclosure/@url').get() or ''
      print("Preview Image: ", news['preview_image'])

      news['source_site_name'] = "Voice Of America"
      print("Source Site Name: ", news['source_site_name'])

      yield news
