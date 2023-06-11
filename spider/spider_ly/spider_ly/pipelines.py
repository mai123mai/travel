# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import csv
import os

import pymysql
from itemadapter import ItemAdapter

# class SpiderLyPipeline:
#     def process_item(self, item, spider):
#         print(item)
#         print(f'-----{item["sid"]}入库成功-----')
#         return item


# 数据存储在csv文件里
from spider_ly import items


# class saveCsvScrapyPipeline(object):
#     def __init__(self):
#         if not os.path.exists('tempData_1.csv'):
#             with open('tempData_1.csv', 'w', newline='') as f:
#                 witer = csv.writer(f)
#                 witer.writerow(
#                     ["sid", "title", "detail_link", "main_img", "address", "level", "feature", "price", "full_address",
#                      "open_time", "video", "images", "degreeLevel", "totalNum", "goodNum", "midNum", "badNum",
#                      "hasImgNum", "starNum", "serviceScoreAvgList", "contents"
#                      ])
#         if not os.path.exists('tempData_comment.csv'):
#             with open('tempData_comment.csv', 'w', newline='') as f:
#                 witer1 = csv.writer(f)
#                 witer1.writerow(
#                     ['sid','dpId','page','degreeLevel', 'totalNum', 'goodNum', 'midNum', 'badNum', 'hasImgNum', 'starNum',
#                      'serviceScoreAvgList', 'dpTagList', "comment_time", "comment_user", "comment_stat",
#                      "comment_cotent", "reply_content"])
#         self.file_f = open('tempData_1.csv', 'a+', newline='', encoding='utf-8')
#         self.csvwriter = csv.writer(self.file_f)
#         self.file_f_1 = open('tempData_comment.csv', 'a+', newline='', encoding='utf-8')
#         self.csvwriter_comment = csv.writer(self.file_f_1)
#
#     def process_item(self, item, spider):
#         if spider.name == 'crawl_scenic':
#             if isinstance(item, items.SpiderLyItem):
#                 self.csvwriter.writerow([
#                     item["sid"],
#                     item["title"],
#                     item["detail_link"],
#                     item["main_img"],
#                     item["address"],
#                     item["level"],
#                     item["feature"],
#                     item["price"],
#                     item["full_address"],
#                     item["open_time"],
#                     item["video"],
#                     item["images"],
#                     item["degreeLevel"],
#                     item["totalNum"],
#                     item["goodNum"],
#                     item["midNum"],
#                     item["badNum"],
#                     item["hasImgNum"],
#                     item["starNum"],
#                     item["serviceScoreAvgList"],
#                     item["contents"],
#                 ])
#                 return item
#         if spider.name == 'crawl_comment':
#             if isinstance(item, items.SpiderCommentItem):
#                 self.csvwriter_comment.writerow([
#                     item["sid"],
#                     item["dpId"],
#                     item["page"],
#                     item["degreeLevel"],
#                     item["totalNum"],
#                     item["goodNum"],
#                     item["midNum"],
#                     item["badNum"],
#                     item["hasImgNum"],
#                     item["starNum"],
#                     item["serviceScoreAvgList"],
#                     item["dpTagList"],
#                     item["comment_time"],
#                     item["comment_user"],
#                     item["comment_stat"],
#                     item["comment_cotent"],
#                     item["reply_content"],
#                 ])
#                 return item
#
#     def close_spider(self, spider):
#         self.file_f.close()
#         self.file_f_1.close()


# 数据存储在mysql文件里

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
