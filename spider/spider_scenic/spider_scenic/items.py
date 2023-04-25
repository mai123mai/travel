# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderScenicItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    sid = scrapy.Field()
    title = scrapy.Field()
    detail_link = scrapy.Field()
    main_img = scrapy.Field()
    address = scrapy.Field()
    level = scrapy.Field()
    feature = scrapy.Field()
    price = scrapy.Field()
    full_address = scrapy.Field()
    open_time = scrapy.Field()
    video = scrapy.Field()
    images = scrapy.Field()
    degreeLevel = scrapy.Field()
    totalNum = scrapy.Field()
    goodNum = scrapy.Field()
    midNum = scrapy.Field()
    badNum = scrapy.Field()
    hasImgNum = scrapy.Field()
    starNum = scrapy.Field()
    serviceScoreAvgList = scrapy.Field()
    # dpTagList = scrapy.Field()
    contents = scrapy.Field()
