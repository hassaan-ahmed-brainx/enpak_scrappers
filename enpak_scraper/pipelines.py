from pymongo import MongoClient
from scrapy.utils.project import get_project_settings
import time

class EnpakScraperPipeline:
  def __init__(self):
    settings = get_project_settings()
    self.client = MongoClient(settings.get('MONGODB_URI'))
    self.db = self.client[settings.get('MONGODB_DATABASE')]
    self.collection = self.db[settings.get('MONGODB_COLLECTION')]

  def process_item(self, item, spider):
    if item['title'] == '' or item['title'] is None or item['title'] == 'CNN en Español' or item['description'] == '' or item['description'] is None:
      spider.logger.warn("Invalid news")
      return

    database_result = self.find_news(item)

    if database_result:
      self.update_news(item)
      spider.logger.debug("Updated news")
    else:
      self.insert_news(item)
      spider.logger.debug("Saved news")

    return item

  def find_news(self, item):
    result = self.collection.find_one({'sourceUrl': item['source_url']})
    if result is None:
      result = self.collection.find_one({'title': item['title']})
    return result

  def insert_news(self, item):
    news = {
      'title': item['title'],
      'publishedDate': item['published_date'] or int(time.time()),
      'author': item['author'] or '',
      'category': item['category'] or '',
      'state': item['state'],
      'continent': item['continent'],
      'description': item['description'] or '',
      'type': item['type'],
      'sourceUrl': item['source_url'],
      'sourceSiteLogo': item['source_site_logo'],
      'previewImage': item['preview_image'] or '',
      'sourceSiteName': item['source_site_name'],
      'postType': 'News',
      'isScrapped': True,
      'createdAt': int(time.time())
    }
    self.collection.insert_one(news)

  def update_news(self, item):
    filter_query = {'sourceUrl': item['source_url']}
    update_query = {
      '$set': {
        'title': item['title'],
        'publishedDate': item['published_date'] or int(time.time()),
        'author': item['author'] or '',
        'category': item['category'] or '',
        'state': item['state'],
        'continent': item['continent'],
        'description': item['description'] or '',
        'type': item['type'],
        'sourceSiteLogo': item['source_site_logo'],
        'previewImage': item['preview_image'] or '',
        'sourceSiteName': item['source_site_name'],
        'updatedAt': int(time.time())
      }
    }
    self.collection.update_one(filter_query, update_query)

  def close_spider(self, spider):
    self.client.close()
