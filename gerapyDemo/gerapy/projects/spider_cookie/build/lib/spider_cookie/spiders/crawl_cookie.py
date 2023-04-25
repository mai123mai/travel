import scrapy
from scrapy import cmdline

from spider_cookie.items import SpiderCookieItem


class CrawlCookieSpider(scrapy.Spider):
    name = 'crawl_cookie'

    # allowed_domains = ['xx.con']
    start_urls = 'https://so.ly.com/scenery/newsearchlist_hot.aspx'
    # start_urls = 'https://www.baidu.com'

    def start_requests(self):
        n = 100
        for i in range(1, n):
            # print(self.start_urls)
            yield scrapy.Request(url=self.start_urls, callback=self.parse, dont_filter=True)

    def parse(self, response):
        # print(response.text)
        item = SpiderCookieItem()
        item['cookie'] = response.text
        yield item


if __name__ == '__main__':
    cmdline.execute("scrapy crawl crawl_cookie --nolog".split())
