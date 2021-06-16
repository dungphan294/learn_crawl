# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TgddItem(scrapy.Item):
    product_name = scrapy.Field()
    price_sale = scrapy.Field()
    price = scrapy.Field()
    rate_average = scrapy.Field
