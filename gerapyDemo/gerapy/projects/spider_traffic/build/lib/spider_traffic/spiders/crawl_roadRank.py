import json
from sqlalchemy import create_engine
from sqlalchemy import text
from datetime import datetime
import pandas as pd
import scrapy
from scrapy import Request, cmdline

from spider_traffic.items import SpiderRoadrankItem


class CrawlRoadrankSpider(scrapy.Spider):
    name = 'crawl_roadRank'
    # allowed_domains = ['aa.com']
    # start_urls = ['http://aa.com/']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        engine = create_engine('mysql+pymysql://root:123456@localhost/dbm')
        con = engine.connect()
        df = pd.read_sql(text('select * from city_code'), con=con)
        self.pd_codes = df[['code', 'name']].values.tolist()

    def start_requests(self):
        headers = {
            "authority": "report.amap.com",
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "referer": "https://report.amap.com/detail.do?city=440100",
            "sec-ch-ua": "\".Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"103\", \"Chromium\";v=\"103\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
            "x-requested-with": "XMLHttpRequest"
        }
        cookies = {
            "user_unique_id": "a185bbc7864ea8e701872db043f30aac",
            "SESSION": "3ca1e5d4-2494-4f2c-8dd8-1379ec2e2f99",
            "UM_distinctid": "1872db04825279-0909f1aed02481-26021a51-1fa400-1872db048268e1",
            "CNZZDATA1256662931": "305016805-1680096682-https%253A%252F%252Freport.amap.com%252F%7C1680100307"
        }
        base_url = "https://report.amap.com/ajax/roadRank.do"

        for i in self.pd_codes:
            code = i[0]
            city_name = i[1]
            for dataType in [0, 1, 2]:
                url = base_url + f'?cityCode={code}&roadType={dataType}&timeType=0'
                yield Request(url,
                              callback=self.parse,
                              meta={'code': code, 'dataType': dataType, 'city_name': city_name},
                              headers=headers,
                              cookies=cookies,
                              dont_filter=True)

    def parse(self, response):
        item = SpiderRoadrankItem()
        json_datas = json.loads(response.text).get('tableData')
        meta = response.meta
        code = meta.get('code')
        dataType = meta.get('dataType')
        city_name = meta.get('city_name')
        temp = []
        for i in json_datas:
            number = i.get('number')
            name = i.get('name')
            dir = i.get('dir')
            index = i.get('index')
            speed = i.get('speed')
            travelTime = i.get('travelTime')
            delayTime = i.get('delayTime')
            temp.append([number, name, dir, index, speed, travelTime, delayTime])
        datas = json.dumps(temp)
        pid = str(code) + '_' + str(dataType)
        times = datetime.now().strftime('%Y-%m-%d %H:%M')
        item['id'] = pid
        item['times'] = times
        item['code'] = code
        item['name'] = city_name
        item['dataType'] = dataType
        item['datas'] = datas
        yield item


if __name__ == '__main__':
    cmdline.execute("scrapy crawl crawl_roadRank --nolog".split())
