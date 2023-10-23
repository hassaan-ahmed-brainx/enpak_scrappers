import scrapy

class NewsItem(scrapy.Item):
  title = scrapy.Field(default='')
  published_date = scrapy.Field(default=0)
  author = scrapy.Field(default='')
  category = scrapy.Field(default='')
  state = scrapy.Field(default='')
  continent = scrapy.Field(default='')
  description = scrapy.Field(default='')
  type = scrapy.Field(default='')
  source_url = scrapy.Field(default='')
  source_site_logo = scrapy.Field(default='')
  preview_image = scrapy.Field(default='')
  source_site_name = scrapy.Field(default='')
  pass
