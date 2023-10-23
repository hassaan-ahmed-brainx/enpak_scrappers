# CNN Spider
# https://edition.cnn.com/

import scrapy
from enpak_scraper.items import NewsItem
from datetime import datetime
import re
from scrapy.utils.project import get_project_settings
settings = get_project_settings()

class CNN_Spider(scrapy.Spider):
  name = "cnn_spider"

  def start_requests(self):
    urls = ["http://rss.cnn.com/rss/edition_americas.rss", "http://rss.cnn.com/rss/edition_asia.rss", "http://rss.cnn.com/rss/edition_europe.rss", "http://rss.cnn.com/rss/edition_africa.rss"]
    yield scrapy.Request(url=urls[0], callback=self.parse_rss, cb_kwargs={'continent': "Americas"})
    yield scrapy.Request(url=urls[1], callback=self.parse_rss, cb_kwargs={'continent': "Asia"})
    yield scrapy.Request(url=urls[2], callback=self.parse_rss, cb_kwargs={'continent': "Europe"})
    yield scrapy.Request(url=urls[3], callback=self.parse_rss, cb_kwargs={'continent': "Africa"})

  def parse_rss(self, response, continent):
    for item in response.xpath('//rss/channel/item'):
      news = NewsItem()

      news['title'] = item.xpath('title/text()').get() or ''
      news['title'] = news['title'].strip().replace('\n', '') if news['title'] else news['title']

      match = re.search(r"/(\d{4})/(\d{2})/(\d{2})", item.xpath('link/text()').get() or '')
      if match:
        year, month, day = map(int, match.groups())
        news['published_date'] = int(datetime(year, month, day).timestamp())
      else:
        news['published_date'] = 0

      news['category'] = "News"

      news['state'] = ''

      news['continent'] = continent

      news['description'] = item.xpath('description/text()').get() or ''

      news['type'] = "International"

      news['source_url'] = item.xpath('link/text()').get() or ''

      news['source_site_logo'] = 'https://w1.pngwing.com/pngs/206/434/png-transparent-logo-cnn-news-logo-of-nbc-media-text-red-line.png'

      news['preview_image'] = item.xpath('media:group/media:content/@url', namespaces=settings.get('NS_MAP')).get() or ''

      news['source_site_name'] = "CNN"

      yield scrapy.Request(url=news['source_url'], callback=self.parse_website, cb_kwargs={'news': news})

  def parse_website(self, response, news):
    news['author'] = response.xpath("//span[@class='byline__name']/text() | p[@data-type='byline-area']/a/text()").get() or ''

    print('\n')
    print("Title: ", news['title'])
    print("Published Date: ", news['published_date'])
    print("Author: ", news['author'])
    print("Category: ", news['category'])
    print("Continent: ", news['continent'])
    print("Description: ", news['description'])
    print("Type: ", news['type'])
    print("Source URL: ", news['source_url'])
    print("Source Site Logo: ", news['source_site_logo'])
    print("Preview Image: ", news['preview_image'])
    print("Source Site Name: ", news['source_site_name'])

    yield news
