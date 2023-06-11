import random
import re
from urllib.parse import urlencode

import scrapy
from scrapy import cmdline

from spider_scenic.items import SpiderCommentItem
from scrapy_redis.spiders import RedisSpider


class CrawlCommentSpider(RedisSpider):
    name = 'crawl_comment'
    # allowed_domains = ['xx.con']
    # start_urls = ['http://xx.con/']

    redis_key = 'comment_url'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.headers = {
            "accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Host": "www.ly.com",
            "Pragma": "no-cache",
            "Referer": "https://www.ly.com/scenery/BookSceneryTicket_20057.html?track=true",
            "sec-ch-ua": "\"Google Chrome\";v=\"111\", \"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"111\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"macOS\"",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "x-requested-with": "XMLHttpRequest"
        }
        cookie_text = "SECKEY_ABVK=3ml12/IL3MzCFdQzDq8xa0Iag1Yj1BJNDSf6d0wZ5TE=; BMAP_SECKEY=3ml12_IL3MzCFdQzDq8xa_IamV4mmwRnfgNU9C6mXddAVYl0WxbQjED8VngIbm5UiAgTEpu_wm1IgPAyg1lbsuW6WzTnyqcaFdkivrscweZcoseSnHXeJgd6JZlWEQ6jumA71Cd8Oibl28pJ-raa5yj53a-GDYX9hwVCW90NVhc0vhxfrLzvAd57h0sjYX7E; H5CookieId=1fca5a4e-75aa-44cd-bf37-3966c655038c; _ga=GA1.2.605122596.1677573761; guolvUserToken=b0ce0cb6-8e2f-4784-bb18-d77ffd8f9c19; _dx_uzZo5y=eb3d5ae63f73cf6584c18ca7b4fcc9f68f34914d36d79673fd32960f20da0d4dddd75015; _dx_captcha_cid=23056845; businessLine=hotel; firsttime=1678157590240; lasttime=1678157605150; abtkey=37f14e92-fbdd-4106-9416-bce2e20fbd8d; _tcudid_v2=ZMadNzjfleVtlmDHekIZBNTogxz68f72xGEwq3tBgBU; NewProvinceId=6; NCid=91; NewProvinceName=广东; NCName=深圳; 17uCNRefId=RefId=6928722&SEFrom=baidu&SEKeyWords=; TicketSEInfo=RefId=6928722&SEFrom=baidu&SEKeyWords=; CNSEInfo=RefId=6928722&tcbdkeyid=&SEFrom=baidu&SEKeyWords=&RefUrl=https://www.baidu.com/link?url=2nd7vO8fYa9Eg3HLVR2ygphiDfYV72JlByJny1IGXWe&wd=&eqid=8a1572230002b02e000000066413424b; Hm_lvt_64941895c0a12a3bdeb5b07863a52466=1676969694,1677573749,1678157479,1678983761; __tctmu=144323752.0.0; __tctmz=144323752.1678983760060.13.1.utmccn=(organic)|utmcmd=organic|utmEsl=gb2312|utmcsr=baidu|utmctr=; longKey=167696968473806; __tctrack=0; Hm_lvt_c6a93e2a75a5b1ef9fb5d4553a2226e5=1677838191,1678157485,1678705420,1678983767; ASP.NET_SessionId=1jmopo2pz2vqpzztobceubve; wwwscenery=4e2eaaef16e5b9246b38c49c8c6872cb; qdid=39264|1|6928722|0a6c16,39264|1|6928722|0a6c16; Hm_lpvt_64941895c0a12a3bdeb5b07863a52466=1678983844; __tctma=144323752.167696968473806.1676969684373.1679222171700.1679229625788.24; __tctmd=144323752.737325; __tctmc=144323752.105514757; Hm_lpvt_c6a93e2a75a5b1ef9fb5d4553a2226e5=1679230635; route=664ddc368a43cb118b8eb59f40e95e2b; __tctmb=144323752.403455535940426.1679230634222.1679230634222.1; __tccgd=144323752.0"
        self.cookies = {data.split('=')[0]: data.split('=')[-1] for data in cookie_text.split('; ')}

    def make_request_from_data(self, data):
        url = data.decode()
        print(url)
        return self.make_requests_from_url(url)

    def make_requests_from_url(self, url):
        '''
        准备开始爬取首页数据
        '''
        self.headers["Referer"] = url
        page = 1
        maps = lambda x: x[0] if x else ''
        sid = int(maps(re.findall('sid=(\d+)&', url)))
        meta = {
            'page': page,
            'sid': sid
        }
        return scrapy.Request(url, headers=self.headers, cookies=self.cookies, callback=self.parse, meta=meta,
                              dont_filter=True)

    def parse(self, response):
        page = response.meta.get('page', 1)
        sid = response.meta.get('sid')
        totalPage = response.meta.get('totalPage', 1)
        comment_json = response.json()
        dpLists = comment_json.get('dpList')
        totalPage_num = comment_json.get('pageInfo', {}).get('totalPage', 0)
        if totalPage_num > totalPage:
            totalPage = totalPage_num
        if not dpLists:
            page = totalPage
            dpLists = []
        for dp in dpLists:
            item = SpiderCommentItem()
            comment_time = dp.get('dpDate')
            comment_user = dp.get('dpUserName')
            comment_stat = dp.get('lineAccess')
            comment_cotent = dp.get('dpContent')
            csReplyList = dp.get('csReplyList')
            dpId = dp.get('dpId')
            reply_content = csReplyList[0].get('replyContent') if csReplyList else None
            item['sid'] = int(sid)
            item['dpId'] = dpId
            item['page'] = int(page)
            item['comment_time'] = comment_time
            item['comment_user'] = comment_user
            item['comment_stat'] = comment_stat
            item['comment_cotent'] = comment_cotent
            item['reply_content'] = reply_content
            yield item
            # 处理翻页
        page += 1
        if page <= totalPage and page < 1000:
            params = {
                "action": "GetDianPingList",
                "sid": str(sid),
                "page": str(page),
                "pageSize": "10",
                "labId": "6",
                "sort": "0",
                "iid": random.random()
            }
            url = "https://www.ly.com/scenery/AjaxHelper/DianPingAjax.aspx" + '?' + urlencode(params)
            yield scrapy.Request(url, headers=self.headers, cookies=self.cookies, callback=self.parse, dont_filter=True,
                                 meta={"sid": sid, 'page': page, 'totalPage': totalPage})


if __name__ == '__main__':
    cmdline.execute("scrapy crawl crawl_comment".split())
