# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import redis
from itemadapter import ItemAdapter


class SpiderCookiePipeline:

    def open_spider(self, spider):
        self.sr = redis.Redis(db=2, host='127.0.0.1', port=6379)

    def close_spider(self, spider):
        # 关闭游标和连接
        self.sr.expire('cookies', 3600 * 24)
        self.sr.close()

    def process_item(self, item, spider):
        try:
            if spider.name == "crawl_cookie":
                self.sr.lpush('cookies', item['cookie'])
                print('push cookie success')
        except:
            print('push cookie fail')
