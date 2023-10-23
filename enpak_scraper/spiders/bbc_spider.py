# BBC Spider
# https://www.bbc.com/

import scrapy
from enpak_scraper.items import NewsItem
from datetime import datetime
import re
from scrapy.utils.project import get_project_settings
settings = get_project_settings()

class BBC_Spider(scrapy.Spider):
  name = "bbc_spider"

  def start_requests(self):
    urls = ["http://feeds.bbci.co.uk/news/world/us_and_canada/rss.xml", "http://feeds.bbci.co.uk/news/world/asia/rss.xml", "http://feeds.bbci.co.uk/news/world/europe/rss.xml", "http://feeds.bbci.co.uk/news/world/africa/rss.xml"]
    yield scrapy.Request(url=urls[0], callback=self.parse_rss, cb_kwargs={'continent': "Americas"})
    yield scrapy.Request(url=urls[1], callback=self.parse_rss, cb_kwargs={'continent': "Asia"})
    yield scrapy.Request(url=urls[2], callback=self.parse_rss, cb_kwargs={'continent': "Europe"})
    yield scrapy.Request(url=urls[3], callback=self.parse_rss, cb_kwargs={'continent': "Africa"})

  def parse_rss(self, response, continent):
    for item in response.xpath('//rss/channel/item'):
      news = NewsItem()

      news['title'] = item.xpath('title/text()').get() or ''
      news['title'] = news['title'].strip().replace('\n', '') if news['title'] else news['title']

      date = item.xpath('pubDate/text()').get() or ''
      if date:
        date = datetime.strptime(date, '%a, %d %b %Y %H:%M:%S %Z')
        news['published_date'] = int(date.timestamp())

      match = re.search(r"/(?:\w+/){0}(\w+)/", item.xpath('link/text()').get() or '')
      news['category'] = match.group(1).capitalize() if match else ''

      news['state'] = ''

      news['continent'] = continent

      news['description'] = item.xpath('description/text()').get() or ''

      news['type'] = "International"

      news['source_url'] = item.xpath('link/text()').get() or ''

      news['source_site_logo'] = 'https://cdn.icon-icons.com/icons2/70/PNG/512/bbc_news_14062.png'

      news['source_site_name'] = "BBC"

      yield scrapy.Request(url=news['source_url'], callback=self.parse_website, cb_kwargs={'news': news})

  def parse_website(self, response, news):
    news['author'] = response.xpath("//div[@class='ssrcss-1u2in0b-Container-ContributorDetails e8mq1e913']/div/text()").get() or ''
    if news['author']:
      news['author'] = news['author'].replace('By', '', 1).strip()

    image_sources = response.xpath("//span[@class='ssrcss-11kpz0x-Placeholder e16icw910']/picture/img/@srcset").get() or ''
    if image_sources:
      image =  image_sources.split(',')[1].strip()
      news['preview_image'] = image.split(' ', 1)[0].strip()
    else:
      news['preview_image'] = ''

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
