# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GamesItem(scrapy.Item):
    name = scrapy.Field()
    sell_price = scrapy.Field()
    sell_total_offers = scrapy.Field()
    historical_price = scrapy.Field()
    product_metadata = scrapy.Field()
