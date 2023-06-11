import random
from urllib.parse import urlencode
import execjs
import redis
import scrapy
from lxml import etree
from scrapy import Request
from scrapy import cmdline
import sys


from spider_scenic.items import SpiderScenicItem
sys.path.append("..")

class CrawlScenicSpider(scrapy.Spider):
    name = 'crawl_scenic'

    # allowed_domains = ['xxx.con']
    start_urls = ['https://so.ly.com/scenery/newsearchlist_hot.aspx']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sr = redis.Redis(db=2, host='127.0.0.1', port=6379)
        self.headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Cookie": "H5CookieId=b7dc51e5-dc7e-446b-90c7-80af8bf730bc; Hm_lvt_64941895c0a12a3bdeb5b07863a52466=1677680764,1678013366; wwwscenery=a180ebce57714784cf3189bd40d04f27; ASP.NET_SessionId=fvddeddma0trjvnnye0huurb; __tctma=144323752.1677680761840189.1677680761742.1678023838908.1678806027547.5; __tctmu=144323752.0.0; __tctmz=144323752.1678806027547.5.1.utmccn=(direct)|utmcsr=(direct)|utmcmd=(none); longKey=1677680761840189; __tctrack=0; 17uCNRefId=RefId=14211829&SEFrom=so&SEKeyWords=; TicketSEInfo=RefId=14211829&SEFrom=so&SEKeyWords=; CNSEInfo=RefId=14211829&tcbdkeyid=&SEFrom=so&SEKeyWords=&RefUrl=https%3A%2F%2Fso.ly.com%2F; Hm_lvt_c6a93e2a75a5b1ef9fb5d4553a2226e5=1677680771,1678013376,1678806777; qdid=28045|1|14211829|40699c,28045|1|14211829|40699c,28045|1|14211829|40699c; Hm_lpvt_c6a93e2a75a5b1ef9fb5d4553a2226e5=1678806815; __tctmb=144323752.1332145759438143.1678806802776.1678806810996.4; __tctmc=144323752.96361118; __tctmd=144323752.737325",
            "Host": "so.ly.com",
            "Pragma": "no-cache",
            "Referer": "https://so.ly.com/scenery/newsearchlist_hot.aspx",
            "sec-ch-ua": "\".Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"103\", \"Chromium\";v=\"103\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
        }
        self.headers2 = {
            "Host": "www.ly.com",
            "sec-ch-ua": "\"Chromium\";v=\"110\", \"Not A(Brand\";v=\"24\", \"Google Chrome\";v=\"110\"",
            "accept": "*/*",
            "x-requested-with": "XMLHttpRequest",
            "sec-ch-ua-mobile": "?0",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
            "sec-ch-ua-platform": "\"macOS\"",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://www.ly.com/scenery/BookSceneryTicket_682134.html",
            "Accept-Language": "zh-CN,zh;q=0.9"
        }
        self.cookies2 = {
            "jq_recsearch": "%E5%8E%A6%E9%97%A8",
            "SECKEY_ABVK": "UMJ9ncJLR6G3hZE2jrIXbOda80Vy4Y9Ip0PbKXttpT4%3D",
            "BMAP_SECKEY": "DAPAUpEyVFMj3UJCWwLATJOgAaaw4_eL4Wp7Wl-9EqFtji8VkqCR2TrcPTEbWcT6M7ln72cgSE4Wm2vDBqtXxtlNZ9xkbGW8K-xZuP49nB8J7RfAfeSI3L7G9-07c6UrGSNDyXFOJM11vimw2bzeA7sxNWx1HmSjkZipAm-mkdZR0aPPd76mX4crjn1oMXgM",
            "NewProvinceId": "6",
            "NCid": "91",
            "NewProvinceName": "%E5%B9%BF%E4%B8%9C",
            "NCName": "%E6%B7%B1%E5%9C%B3",
            "__tctmu": "144323752.0.0",
            "longKey": "167696968473806",
            "__tctrack": "0",
            "Hm_lvt_64941895c0a12a3bdeb5b07863a52466": "1676969694,1677573749",
            "H5CookieId": "1fca5a4e-75aa-44cd-bf37-3966c655038c",
            "Hm_lvt_c6a93e2a75a5b1ef9fb5d4553a2226e5": "1677573758",
            "dj-meta": "%257B%2522ttf%2522%3A%252211011010110111110001001101111100010110011111000%257C1011011110000001101000%2522%2C%2522tz%2522%3A-480%2C%2522au%2522%3A%252248000_2_1_0_2_explicit_speakers%2522%2C%2522gp%2522%3A%2522Google%2520Inc.%2520(Intel%2520Inc.)%40ANGLE%2520(Intel%2520Inc.%2C%2520Intel(R)%2520Iris(TM)%2520Plus%2520Graphics%2520OpenGL%2520Engine%2C%2520OpenGL%25204.1)%2522%2C%2522cv%2522%3A%25222d58a52d428e99d1e377c9376b06732049d1ef27%2522%2C%2522pls%2522%3A%2522PDF%2520ViewerChrome%2520PDF%2520ViewerChromium%2520PDF%2520ViewerMicrosoft%2520Edge%2520PDF%2520ViewerWebKit%2520builtin%2520PDF%2522%2C%2522hd%2522%3A%2522zh-CN_zh_8%2522%2C%2522sc%2522%3A%2522900_1440_30_2%2522%2C%2522ua%2522%3A%2522Mozilla%2F5.0%2520(Macintosh%3B%2520Intel%2520Mac%2520OS%2520X%252010_15_7)%2520AppleWebKit%2F537.36%2520(KHTML%2C%2520like%2520Gecko)%2520Chrome%2F110.0.0.0%2520Safari%2F537.36%2522%2C%2522ft%2522%3A%25229ed34b46ca3c1706db122622a6685455e3f082e7%2522%2C%2522lg%2522%3A%25224a95d43fd6e3dc68abc0444e278484fc8432c22c%2522%257D",
            "_ga": "GA1.2.605122596.1677573761",
            "__tctmz": "144323752.1677652965859.3.2.utmccn=(referral)|utmcsr=google.com|utmcct=|utmcmd=referral",
            "ASP.NET_SessionId": "tgl34xlz5silml3m2vrwyvne",
            "session": "4d3c193d-90d7-4f04-b33f-b0edfdcc11f3",
            "guolvUserToken": "b0ce0cb6-8e2f-4784-bb18-d77ffd8f9c19",
            "dj_current_src": "%7B%22CityId%22%3A%2291%22%2C%22CityArea%22%3A%22%E5%8D%8E%E5%8D%97%22%2C%22CityName%22%3A%22%E6%B7%B1%E5%9C%B3%22%2C%22FullPinyinName%22%3A%22shenzhen%22%2C%22FirstZiMu%22%3A%22S%22%2C%22ProvinceId%22%3A%226%22%2C%22ProvinceName%22%3A%22%E5%B9%BF%E4%B8%9C%22%2C%22ShortPy%22%3A%22sz%22%2C%22TcShortPy%22%3A%22shz%22%7D",
            "wwwscenery": "4e2eaaef16e5b9246b38c49c8c6872cb",
            "_dx_uzZo5y": "eb3d5ae63f73cf6584c18ca7b4fcc9f68f34914d36d79673fd32960f20da0d4dddd75015",
            "_dx_captcha_cid": "23056845",
            "udc_feedback": "%7B%22url%22%3A%20%22https%3A%2F%2Fgny.ly.com%2F%22%2C%22platform%22%3A%20%22PC%22%2C%22channel%22%3A%20%22%E5%9B%BD%E5%86%85%E6%B8%B8%22%2C%22page%22%3A%20%22%E5%9B%BD%E5%86%85%E8%AF%A6%E6%83%85%E9%A1%B5%22%7D",
            "pt__search_from": "channel=scenery&page=scenery-index",
            "pagestate": "1",
            "Hm_lpvt_64941895c0a12a3bdeb5b07863a52466": "1677657686",
            "indexTopSearchHistory": "%5B%22%E5%9B%9B%E5%B7%9D%22%2C%22%E5%8E%A6%E9%97%A8%22%5D",
            "17uCNRefId": "RefId=14211829&SEFrom=so&SEKeyWords=",
            "TicketSEInfo": "RefId=14211829&SEFrom=so&SEKeyWords=",
            "CNSEInfo": "RefId=14211829&tcbdkeyid=&SEFrom=so&SEKeyWords=&RefUrl=https%3A%2F%2Fso.ly.com%2F",
            "qdid": "28045|1|14211829|40699c,28045|1|14211829|40699c,28045|1|14211829|40699c",
            "__tccgd": "144323752.0",
            "__tctma": "144323752.167696968473806.1676969684373.1677657690291.1677736163929.5",
            "Hm_lpvt_c6a93e2a75a5b1ef9fb5d4553a2226e5": "1677737771",
            "route": "a14e2b278f3edf5ed22249307678b7ac",
            "__tctmc": "144323752.8709683",
            "__tctmd": "144323752.95395742",
            "__tctmb": "144323752.3320320891517118.1677737704638.1677737726698.8"
        }
        self.page = 1
        self.pageCount = 1113
        # current_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # path = f'{current_path}/xxx.js'
        path = r'E:\tuling\tl\travel\spider\spider_scenic\spider_scenic\xxx.js'
        self.js_text = open(path, 'r', encoding='UTF-8').read()

    def start_requests(self):
        temp = self.get_cookie()
        cookies = {data.split('=')[0]: data.split('=')[-1] for data in temp.split('; ')}
        dctrack = execjs.compile(self.js_text).call('get_dctrack', temp)
        params = {
            "action": "getlist",
            "page": str(self.page),
            "q": "",
            "pid": "0",
            "c": "0",
            "cyid": "0",
            "sort": "2",
            "isnow": "0",
            "spType": "",
            "lbtypes": "",
            "IsNJL": "0",
            "classify": "",
            "grade": "",
            "dctrack": dctrack,
            "iid": random.random()
        }
        url = 'https://so.ly.com/scenery/newsearchlist_hot.aspx' + '?' + urlencode(params)
        yield Request(url,
                      callback=self.parse,
                      headers=self.headers,
                      cookies=cookies,
                      dont_filter=True)

    def parse(self, response):
        flag_end = response.xpath('//p[@class="p01"]/text()').extract_first()
        if flag_end:
            if '很抱歉，没有找到' in response.xpath('//p[@class="p01"]/text()').extract_first():
                print('已到最后一页')
                return ''
        scenery_list = response.xpath('//div[@class="scenery_list"]')
        for i, scenery in enumerate(scenery_list):
            item = SpiderScenicItem()
            sid = scenery.xpath('./div/div[@class="s_info"]/@sid').extract_first()
            if sid.isdigit():
                sid = int(sid)
            detail_link = 'https:' + scenery.xpath('./div/div[@class="s_info"]/a/@href').extract_first()
            main_img = 'https:' + scenery.xpath('./div/div[@class="s_info"]/a/img/@src').extract_first()
            address_list = scenery.xpath(
                './div/div[@class="s_info"]//span[@class="sce_address"]/a/text()').extract()
            address = ','.join(address_list)
            level = scenery.xpath('./div/div[@class="s_info"]//span[@class="s_level"]/text()').extract_first()
            feature = scenery.xpath(
                './div/div[@class="s_info"]//div[@class="info_c"]//dd[last()]/p/text()').extract_first()
            price = scenery.xpath('./div/div[@class="s_info"]//div[@class="price_b"]/span/b/text()').extract_first()
            item['sid'] = sid
            item['detail_link'] = detail_link
            item['main_img'] = main_img
            item['address'] = address
            item['level'] = level
            item['feature'] = feature
            item['price'] = price
            yield scrapy.Request(detail_link,
                                 callback=self.parse_detail,
                                 meta={"item": item, 'i': i, 'sid': sid})
        # 处理翻页
        if self.page < self.pageCount:
            self.page += 1
            temp = self.get_cookie()
            cookies = {data.split('=')[0]: data.split('=')[-1] for data in temp.split('; ')}
            dctrack = execjs.compile(self.js_text).call('get_dctrack', temp)
            params = {
                "action": "getlist",
                "page": str(self.page),
                "q": "",
                "pid": "0",
                "c": "0",
                "cyid": "0",
                "sort": "2",
                "isnow": "0",
                "spType": "",
                "lbtypes": "",
                "IsNJL": "0",
                "classify": "",
                "grade": "",
                "dctrack": dctrack,
                "iid": random.random()
            }
            url = 'https://so.ly.com/scenery/newsearchlist_hot.aspx' + '?' + urlencode(params)
            yield scrapy.Request(url, callback=self.parse, cookies=cookies)

    def parse_detail(self, response):
        item = response.meta["item"]
        i = response.meta["i"]
        sid = item.get('sid')
        title = response.xpath('//h3[@class="s_name"]/text()').extract_first()
        if title:
            title = title.strip()
        full_address = response.xpath('//p[contains(@class,"s_address")]/span/text()').extract_first()
        if full_address:
            full_address = full_address.strip()
        open_time = response.xpath('//div[contains(@class,"s-tShow mt10")]/pre/text()').extract_first()
        if open_time:
            open_time = open_time.replace('\r\n', ' | ')
        video = response.xpath('//video[@id="myvideo"]/@src').extract_first()
        image_list = response.xpath('//div[@class="img_s_ul"]/ul//img/@bigsrc').extract()
        images = ['https:' + i for i in image_list]
        info_list = response.xpath('//div[@class="inf-f-con"]/div').extract_first()
        if info_list:
            contents = self.get_info(info_list)
        else:
            contents = ''
        item['title'] = title
        item['full_address'] = full_address
        item['open_time'] = open_time
        item['video'] = video
        item['images'] = str(images)
        item['contents'] = str(contents)
        params = {
            "action": "GetDianPingList",
            "sid": sid,
            "page": '1',
            "pageSize": "10",
            "labId": "1",
            "sort": "0",
            "iid": random.random()
        }
        comment_url = "https://www.ly.com/scenery/AjaxHelper/DianPingAjax.aspx" + '?' + urlencode(params)
        yield scrapy.Request(comment_url, headers=self.headers2,
                             cookies=self.cookies2, callback=self.parse_comment,
                             meta={"item": item, 'i': i})

    def parse_comment(self, response):
        item = response.meta["item"]
        i = response.meta["i"]
        comment_json = response.json()
        degreeLevel = comment_json.get('degreeLevel')
        totalNum = comment_json.get('totalNum')
        goodNum = comment_json.get('goodNum')
        midNum = comment_json.get('midNum')
        badNum = comment_json.get('badNum')
        hasImgNum = comment_json.get('hasImgNum')
        starNum = comment_json.get('starNum')
        serviceScoreAvgList = comment_json.get('serviceScoreAvgList')
        # dpTagList = comment_json.get('dpTagList')
        item['degreeLevel'] = degreeLevel
        item['totalNum'] = totalNum
        item['goodNum'] = goodNum
        item['midNum'] = midNum
        item['badNum'] = badNum
        item['hasImgNum'] = hasImgNum
        item['starNum'] = starNum
        item['serviceScoreAvgList'] = str(serviceScoreAvgList)
        # item['dpTagList'] = str(dpTagList)
        print(item)
        yield item

    def get_info(self, infos):
        maps = lambda x: x[0] if x else ''
        infos = etree.HTML(infos)
        contents = list()
        for info in infos:
            info_title = maps(info.xpath('./h4/text()'))
            info_content = ' | '.join(info.xpath('./div/p/text()'))
            info_img = info.xpath('./div/div[@class="info-img-w"]/img/@orisrc')
            info_image = ' | '.join(["https:" + i for i in info_img])
            content = {
                "info_title": info_title,
                "info_content": info_content,
                "info_image": info_image,
            }
            contents.append(content)
        return contents

    def get_cookie(self):
        """
        获取cookie
        """
        maps = lambda x: x[0].decode() if x else None
        cookies = maps(self.sr.lrange('cookies', 0, 0))
        if cookies:
            # print(cookies)
            self.sr.lpop('cookies')
            self.sr.rpush('cookies', cookies)
            return cookies

if __name__ == '__main__':
    cmdline.execute("scrapy crawl crawl_scenic".split())

