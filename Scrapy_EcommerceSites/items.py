# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NutItem(scrapy.Item):
    brand = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    price = scrapy.Field()
    main_image_url = scrapy.Field()
    additional_image_urls = scrapy.Field()
    sku = scrapy.Field()
    category = scrapy.Field()
