# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymysql
from itemadapter import ItemAdapter


# class SpiderTrafficPipeline:
#     def process_item(self, item, spider):
#         return item
from spider_traffic import items


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
        if spider.name == "crawl_traffic":
            if isinstance(item, items.SpiderTrafficItem):
                try:
                    sql = '''replace into traffic_congestion_index values (%s,%s,%s,%s,%s,%s)'''
                    self.cursor.execute(sql, (
                        item["id"],
                        item["times"],
                        item["code"],
                        item["name"],
                        item["dataType"],
                        item["datas"],
                    ))
                    # 提交
                    self.conn.commit()
                    print(f'入库-->{item}')
                except Exception as e:
                    self.conn.rollback()
                    print('信息写入错误%s-%s' % (item['sid'], e))

        if spider.name == "crawl_districtRank":
            if isinstance(item, items.SpiderDistrictItem):
                try:
                    sql = '''replace into traffic_district_rank values (%s,%s,%s,%s,%s,%s)'''
                    self.cursor.execute(sql, (
                        item["id"],
                        item["times"],
                        item["code"],
                        item["name"],
                        item["dataType"],
                        item["datas"],
                    ))
                    # 提交
                    self.conn.commit()
                    print(f'入库-->{item}')
                except Exception as e:
                    self.conn.rollback()
                    print('信息写入错误%s-%s' % (item['sid'], e))

        if spider.name == "crawl_roadRank":
            if isinstance(item, items.SpiderRoadrankItem):
                try:
                    sql = '''replace into traffic_roadrank_rank values (%s,%s,%s,%s,%s,%s)'''
                    self.cursor.execute(sql, (
                        item["id"],
                        item["times"],
                        item["code"],
                        item["name"],
                        item["dataType"],
                        item["datas"],
                    ))
                    # 提交
                    self.conn.commit()
                    print(f'入库-->{item}')
                except Exception as e:
                    self.conn.rollback()
                    print('信息写入错误%s-%s' % (item['sid'], e))


        if spider.name == "crawl_mapData":
            if isinstance(item, items.SpiderMapdataItem):
                try:
                    sql = '''replace into traffic_map values (%s,%s,%s,%s,%s,%s)'''
                    self.cursor.execute(sql, (
                        item["cityCode"],
                        item["times"],
                        item["name"],
                        item["center"],
                        item["max_data"],
                        item["data"],
                    ))
                    # 提交
                    self.conn.commit()
                    print(f'入库-->{item}')
                except Exception as e:
                    self.conn.rollback()
                    print('信息写入错误%s-%s' % (item['sid'], e))
