import scrapy


class CrawlCommentSpider(scrapy.Spider):
    name = 'crawl_comment'
    allowed_domains = ['xx.con']
    start_urls = ['http://xx.con/']

    def parse(self, response):
        pass
