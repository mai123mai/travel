import json
from datetime import datetime
import pandas as pd
import scrapy
from scrapy import Request, cmdline
from sqlalchemy import create_engine
from sqlalchemy import text

from spider_traffic.items import SpiderMapdataItem


class CrawlMapdataSpider(scrapy.Spider):
    name = 'crawl_mapData'
    # allowed_domains = ['aa.com']
    # start_urls = ['http://aa.com/']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        engine = create_engine('mysql+pymysql://root:123456@localhost/dbm')
        con = engine.connect()
        df = pd.read_sql(text('select * from city_code'), con=con)
        self.pd_codes = df[['code','name']].values.tolist()


    def start_requests(self):
        headers = {
            "authority": "report.amap.com",
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "referer": "https://report.amap.com/detail.do?city=110000",
            "sec-ch-ua": "^\\^.Not/A)Brand^^;v=^\\^99^^, ^\\^Google",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "^\\^Windows^^",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
            "x-requested-with": "XMLHttpRequest"
        }
        cookies = {
            "UM_distinctid": "1872db04825279-0909f1aed02481-26021a51-1fa400-1872db048268e1",
            "user_unique_id": "a187bf65864ea91c0187a944eda41110",
            "SESSION": "6f6d7e3a-7a29-4482-965d-b01814729370",
            "cna": "I7fRGwPZpWMCAXBdjtaRKPpC",
            "xlly_s": "1",
            "gray_auth": "2",
            "passport_login": "NTI0MzUzODE5LGFtYXBfMTM0MTY4NDIzMzdCSXdMRVZjNUEsZWNzczJwYmZrYWkyN3RqdmR1M3Y3YzRzZHhtczdtbGcsMTY4MjE3MjQzMixaVFprWXpZeFlqTmlZV001TkRWaE1tTmlNekV4TkRrM01USTJOVGM0T1RBPQ^%^3D^%^3D",
            "isg": "BAwM2-wphByJfpBg_1ydlWfb3Wo-RbDvWVS3OmbOLrec8an7jlC1fl4AlflJuehH",
            "l": "fBTBou7mNYW_LRsKBO5ZKurza77teQOfCsPzaNbMiIEGa6t5OeY2RNC_iGnW5dtjgT5EWetPUcfRbdFwrVz38FkDBeYCfGjVEd9e7e16nezA.",
            "tfstk": "cfAcB3w0HKWfwch9Vn1jTmj6sRldaCNNxCRWa43w8UWBI-A5usj0UJ55X4jmAmy1.",
            "CNZZDATA1256662931": "305016805-1680096682-https^%^253A^%^252F^%^252Freport.amap.com^%^252F^%^7C1682172355"
        }
        base_url = "https://report.amap.com/ajax/districtRank.do"

        for i in self.pd_codes:
            code = i[0]
            city_name = i[1]
            url = base_url + f'?cityCode={code}&linksType=1'
            yield Request(url,
                          callback=self.parse,
                          meta={'code': code, 'city_name': city_name},
                          headers=headers,
                          cookies=cookies,
                          dont_filter=True)

    def parse(self, response):
        item = SpiderMapdataItem()
        json_datas = json.loads(response.text)
        meta = response.meta
        code = meta.get('code')
        city_name = meta.get('city_name')
        mapdata = []
        data_value = []
        for d in json_datas:
            coords = d.get('coords')[0][0]
            data = d.get('index')
            data_value.append(data)
            for c in coords:
                data_map = {'lat': c.get('lat'), 'lng': c.get('lon'), 'count': data}
                mapdata.append(data_map)
        center = str([mapdata[0].get('lng'), mapdata[0].get('lat')])
        data = json.dumps(mapdata)
        max_data = data_value[0]
        times = datetime.now().strftime('%Y-%m-%d %H:%M')
        item['cityCode'] = code
        item['times'] = times
        item['name'] = city_name
        item['center'] = center
        item['max_data'] = max_data
        item['data'] = data
        yield item


if __name__ == '__main__':
    cmdline.execute("scrapy crawl crawl_mapData --nolog".split())

