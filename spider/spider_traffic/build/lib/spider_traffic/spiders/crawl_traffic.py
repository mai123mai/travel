import json
from sqlalchemy import create_engine
from sqlalchemy import text
import time
from datetime import datetime
import pandas as pd
import scrapy
from scrapy import Request, cmdline

from spider_traffic.items import SpiderTrafficItem


class CrawlTrafficSpider(scrapy.Spider):
    name = 'crawl_traffic'

    # allowed_domains = ['xxx.cn']
    # start_urls = ['http://xxx.cn/']

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
            "referer": "https://report.amap.com/detail.do?city=110000",
            "sec-ch-ua": "\"Google Chrome\";v=\"111\", \"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"111\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"macOS\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
            "x-requested-with": "XMLHttpRequest"
        }
        cookies = {
            "UM_distinctid": "186c4403e38c6a-0a3bdde65878a-1f525634-13c680-186c4403e391164",
            "cna": "+I7mGwN/qg0CAXeT1UkgDPIu",
            "isg": "BCUlEPISrTyYV8lgnDcXzT2jNOdfYtn0hXxYLCcK9txoPkWw77bxxLHfzKJIPvGs",
            "l": "fBa6Q9QgNNEsl7EYBOfZPurza779bIRAguPzaNbMi9fPO6fBsNKAW1MtnvL6CnGVFsZeR3JGlUzkBeYBc3K-nxvtgC4K1AkmnmOk-Wf..",
            "tfstk": "cNlPBdOidWmb1EupXSVEQKgXTQuRZOli9izQEHONtMVlV82liMILoJFU3R_Vx8f..",
            "user_unique_id": "a187bf65864ea91c01872bfd30b61830",
            "SESSION": "79566f6d-7438-4300-b9cd-bbe6feeca5ed",
            "CNZZDATA1256662931": "1961980615-1678328734-https%253A%252F%252Freport.amap.com%252F%7C1680074937"
        }
        base_url = "https://report.amap.com/ajax/cityHourly.do"

        for i in self.pd_codes:
            code = i[0]
            name = i[1]
            for dataType in range(1, 5):
                url = base_url + f'?cityCode={code}&dataType={dataType}'
                yield Request(url,
                              callback=self.parse,
                              meta={'code': code, 'dataType': dataType, 'name': name},
                              headers=headers,
                              cookies=cookies,
                              dont_filter=True)

    def parse(self, response):
        item = SpiderTrafficItem()
        datas = json.loads(response.text)
        meta = response.meta
        code = meta.get('code')
        dataType = meta.get('dataType')
        name = meta.get('name')
        for data in datas:
            timeStap = data[0] * 0.001
            local_time = time.localtime(timeStap)
            t = time.strftime("%Y-%m-%d %H:%M", local_time)
            data[0] = t
        datas = json.dumps(datas)
        times = datetime.now().strftime('%Y-%m-%d %H:%M')
        pid = str(code) + '_' + str(dataType)
        item['id'] = pid
        item['times'] = times
        item['code'] = code
        item['name'] = name
        item['dataType'] = dataType
        item['datas'] = datas
        yield item


if __name__ == '__main__':
    cmdline.execute("scrapy crawl crawl_traffic --nolog".split())
