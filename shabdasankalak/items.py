# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class EkantipurScraperItem(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    date = scrapy.Field()
    place = scrapy.Field()
    category = scrapy.Field()
    content = scrapy.Field()
    url = scrapy.Field()

