# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Article(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    domain = scrapy.Field()
    topic = scrapy.Field()
    source = scrapy.Field()
    description = scrapy.Field()
    content = scrapy.Field()
    author = scrapy.Field()
    date = scrapy.Field()
    thumbnail = scrapy.Field()
