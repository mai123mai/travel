import os
import random
from urllib.parse import urlencode
import execjs
import scrapy
from lxml import etree
from scrapy import Request
from scrapy import cmdline



class CrawlScenicSpider(scrapy.Spider):
    name = 'crawl_scenic'

    # allowed_domains = ['xxx.con']
    start_urls = ['http://baidu.com/']

    def parse(self, response):
        print(response.text)




if __name__ == '__main__':
    cmdline.execute("scrapy crawl crawl_scenic".split())
