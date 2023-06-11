# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymysql
from itemadapter import ItemAdapter


from spider_scenic import items

class saveMysqlScrapyPipeline:

    def open_spider(self, spider):
        data_config = spider.settings['DATA_CONFIG']
        self.conn = pymysql.connect(**data_config['config'])
        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        # 关闭游标和连接
        self.cursor.close()
        self.conn.close()

    def process_item(self, item, spider):
        # 插入数到数据库
        if spider.name == "crawl_scenic":
            if isinstance(item, items.SpiderScenicItem):
                try:
                    sql = '''insert into travel values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
                    self.cursor.execute(sql, (
                        0,
                        item["sid"],
                        item["title"],
                        item["detail_link"],
                        item["main_img"],
                        item["address"],
                        item["level"],
                        item["feature"],
                        item["price"],
                        item["full_address"],
                        item["open_time"],
                        item["video"],
                        item["images"],
                        item["degreeLevel"],
                        item["totalNum"],
                        item["goodNum"],
                        item["midNum"],
                        item["badNum"],
                        item["hasImgNum"],
                        item["starNum"],
                        item["serviceScoreAvgList"],
                        item["contents"]
                    ))
                    # 提交
                    self.conn.commit()
                    print(f'入库-->{item}')
                except Exception as e:
                    self.conn.rollback()
                    print('信息写入错误%s-%s' % (item['sid'], e))
        if spider.name == 'crawl_comment':
            if isinstance(item, items.SpiderCommentItem):
                try:
                    sql = '''insert into comments values (%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
                    self.cursor.execute(sql, (
                        0,
                        item["sid"],
                        item["dpId"],
                        item["page"],
                        item["comment_time"],
                        item["comment_user"],
                        item["comment_stat"],
                        item["comment_cotent"],
                        item["reply_content"]
                    ))
                    # 提交
                    self.conn.commit()
                    print(f'入库-->{item}')
                except Exception as e:
                    self.conn.rollback()
                    print('信息写入错误%s-%s' % (item['sid'], e))

