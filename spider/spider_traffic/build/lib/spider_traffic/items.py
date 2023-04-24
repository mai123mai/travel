# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderTrafficItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    times = scrapy.Field()
    code = scrapy.Field()
    name = scrapy.Field()
    dataType = scrapy.Field()
    datas = scrapy.Field()


class SpiderDistrictItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    times = scrapy.Field()
    code = scrapy.Field()
    name = scrapy.Field()
    dataType = scrapy.Field()
    datas = scrapy.Field()

class SpiderRoadrankItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    times = scrapy.Field()
    code = scrapy.Field()
    name = scrapy.Field()
    dataType = scrapy.Field()
    datas = scrapy.Field()


class SpiderMapdataItem(scrapy.Item):
    # define the fields for your item here like:
    # cityCode, times, name, center, max_data, data
    cityCode = scrapy.Field()
    times = scrapy.Field()
    name = scrapy.Field()
    center = scrapy.Field()
    max_data = scrapy.Field()
    data = scrapy.Field()
