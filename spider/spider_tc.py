import csv
import os
import random
import execjs
import requests
from lxml import etree
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('mysql+pymysql://root:123456@localhost/dbm')


class Spider:
    def __init__(self):
        self.page = 1
        self.spider_url = "https://so.ly.com/scenery/newsearchlist_hot.aspx"
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
        if not os.path.exists('tempData_2.csv'):
            with open('tempData_2.csv', 'w', newline='') as f:
                witer = csv.writer(f)
                witer.writerow(
                    ["sid", "title", "detail_link", "main_img", "address", "level", "feature", "price", "full_address",
                     "open_time", "video", "images", "degreeLevel", "totalNum", "goodNum", "midNum", "badNum",
                     "hasImgNum", "starNum", "serviceScoreAvgList", "dpTagList", "contents"
                     ])
        if not os.path.exists('./comment_1.csv'):
            with open('./comment_1.csv', 'w', newline='') as f:
                witer = csv.writer(f)
                witer.writerow(['sid', 'degreeLevel', 'totalNum', 'goodNum', 'midNum', 'badNum', 'hasImgNum', 'starNum',
                                'serviceScoreAvgList', 'dpTagList', "comment_time", "comment_user", "comment_stat",
                                "comment_cotent", "reply_content"])
        # try:
        #     sql = '''
        #     CREATE TABLE movie(
        #                         id int PRIMARY KEY AUTO_INCREMENT,
        #                         movie_id varchar(255),
        #                         directors varchar(255),
        #                         rate varchar(255),
        #                         title varchar(255),
        #                         casts varchar(255),
        #                         cover varchar(255),
        #                         detaillink varchar(255),
        #                         years varchar(255),
        #                         types varchar(255),
        #                         country varchar(255),
        #                         lang varchar(255),
        #                         pulish_time varchar(255),
        #                         movieTime varchar(255),
        #                         comment_len varchar(255),
        #                         starts varchar(255),
        #                         summary text,
        #                         comments text,
        #                         imglist text,
        #                         movieUrl varchar(255)
        #                 )
        #     '''
        #     cur = conn.cursor()
        #     cur.execute(sql)
        #     conn.commit()
        # except:
        #     pass

        if not os.path.exists(f'./spiderPage.txt'):
            with open(f'./spiderPage.txt', 'w', encoding='utf-8') as f:
                f.write('1\n')

        file_f = open('tempData_2.csv', 'a+', newline='', encoding='utf-8')
        self.save_writer = csv.writer(file_f)

    def get_page(self):
        with open(f'./spiderPage.txt', 'r')as r_f:
            return r_f.readlines()[-1].strip()

    def set_page(self, newPage):
        with open(f'./spiderPage.txt', 'a+')as w_f:
            w_f.write(str(newPage) + '\n')

    def get_detail_text(self, url):
        headers = {
            "Host": "www.ly.com",
            "Connection": "keep-alive",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "sec-ch-ua": "\"Chromium\";v=\"110\", \"Not A(Brand\";v=\"24\", \"Google Chrome\";v=\"110\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"macOS\"",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Sec-Fetch-Site": "same-site",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            "Referer": "https://so.ly.com/",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cookie": "jq_recsearch=%E5%8E%A6%E9%97%A8; SECKEY_ABVK=UMJ9ncJLR6G3hZE2jrIXbN9IsEJw+WNYAqBXV650csc%3D; BMAP_SECKEY=DAPAUpEyVFMj3UJCWwLATBlDGdAHSo9sUAWdfjgjSREjLb1ESqkK63BSvEpdLhw3iW3f7jFugcqMdlQFew02mCv5X7fpmP0ubNTt81dxfic0CfmKun37g_B4EaajHY22sFxFyk75B7ekLyaKo_RXP_670VymOwsyN38iOcbJsG2PpvmSR6-HK1cEiT2htIbj; NewProvinceId=6; NCid=91; NewProvinceName=%E5%B9%BF%E4%B8%9C; NCName=%E6%B7%B1%E5%9C%B3; __tctmu=144323752.0.0; longKey=167696968473806; __tctrack=0; Hm_lvt_64941895c0a12a3bdeb5b07863a52466=1676969694,1677573749; H5CookieId=1fca5a4e-75aa-44cd-bf37-3966c655038c; Hm_lvt_c6a93e2a75a5b1ef9fb5d4553a2226e5=1677573758; dj-meta=%257B%2522ttf%2522%3A%252211011010110111110001001101111100010110011111000%257C1011011110000001101000%2522%2C%2522tz%2522%3A-480%2C%2522au%2522%3A%252248000_2_1_0_2_explicit_speakers%2522%2C%2522gp%2522%3A%2522Google%2520Inc.%2520(Intel%2520Inc.)%40ANGLE%2520(Intel%2520Inc.%2C%2520Intel(R)%2520Iris(TM)%2520Plus%2520Graphics%2520OpenGL%2520Engine%2C%2520OpenGL%25204.1)%2522%2C%2522cv%2522%3A%25222d58a52d428e99d1e377c9376b06732049d1ef27%2522%2C%2522pls%2522%3A%2522PDF%2520ViewerChrome%2520PDF%2520ViewerChromium%2520PDF%2520ViewerMicrosoft%2520Edge%2520PDF%2520ViewerWebKit%2520builtin%2520PDF%2522%2C%2522hd%2522%3A%2522zh-CN_zh_8%2522%2C%2522sc%2522%3A%2522900_1440_30_2%2522%2C%2522ua%2522%3A%2522Mozilla%2F5.0%2520(Macintosh%3B%2520Intel%2520Mac%2520OS%2520X%252010_15_7)%2520AppleWebKit%2F537.36%2520(KHTML%2C%2520like%2520Gecko)%2520Chrome%2F110.0.0.0%2520Safari%2F537.36%2522%2C%2522ft%2522%3A%25229ed34b46ca3c1706db122622a6685455e3f082e7%2522%2C%2522lg%2522%3A%25224a95d43fd6e3dc68abc0444e278484fc8432c22c%2522%257D; _ga=GA1.2.605122596.1677573761; __tctmz=144323752.1677652965859.3.2.utmccn=(referral)|utmcsr=google.com|utmcct=|utmcmd=referral; ASP.NET_SessionId=tgl34xlz5silml3m2vrwyvne; session=4d3c193d-90d7-4f04-b33f-b0edfdcc11f3; guolvUserToken=b0ce0cb6-8e2f-4784-bb18-d77ffd8f9c19; dj_current_src=%7B%22CityId%22%3A%2291%22%2C%22CityArea%22%3A%22%E5%8D%8E%E5%8D%97%22%2C%22CityName%22%3A%22%E6%B7%B1%E5%9C%B3%22%2C%22FullPinyinName%22%3A%22shenzhen%22%2C%22FirstZiMu%22%3A%22S%22%2C%22ProvinceId%22%3A%226%22%2C%22ProvinceName%22%3A%22%E5%B9%BF%E4%B8%9C%22%2C%22ShortPy%22%3A%22sz%22%2C%22TcShortPy%22%3A%22shz%22%7D; wwwscenery=4e2eaaef16e5b9246b38c49c8c6872cb; _dx_uzZo5y=eb3d5ae63f73cf6584c18ca7b4fcc9f68f34914d36d79673fd32960f20da0d4dddd75015; _dx_captcha_cid=23056845; udc_feedback=%7B%22url%22%3A%20%22https%3A%2F%2Fgny.ly.com%2F%22%2C%22platform%22%3A%20%22PC%22%2C%22channel%22%3A%20%22%E5%9B%BD%E5%86%85%E6%B8%B8%22%2C%22page%22%3A%20%22%E5%9B%BD%E5%86%85%E8%AF%A6%E6%83%85%E9%A1%B5%22%7D; pt__search_from=channel=scenery&page=scenery-index; pagestate=1; Hm_lpvt_64941895c0a12a3bdeb5b07863a52466=1677657686; indexTopSearchHistory=%5B%22%E5%9B%9B%E5%B7%9D%22%2C%22%E5%8E%A6%E9%97%A8%22%5D; 17uCNRefId=RefId=14211829&SEFrom=so&SEKeyWords=; TicketSEInfo=RefId=14211829&SEFrom=so&SEKeyWords=; CNSEInfo=RefId=14211829&tcbdkeyid=&SEFrom=so&SEKeyWords=&RefUrl=https%3A%2F%2Fso.ly.com%2F; qdid=28045|1|14211829|40699c,28045|1|14211829|40699c,28045|1|14211829|40699c; __tccgd=144323752.0; __tctma=144323752.167696968473806.1676969684373.1677657690291.1677736163929.5; __tctmb=144323752.3320320891517118.1677737647018.1677737704638.7; __tctmc=144323752.100710275; __tctmd=144323752.205791637; route=36deacbf19e769c54478320fe8c5c7ef; Hm_lpvt_c6a93e2a75a5b1ef9fb5d4553a2226e5=1677737734"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            raise response.status_code

    def js_from_file(self, file_name):
        with open(file_name, 'r', encoding='UTF-8') as file:
            result = file.read()
        return result

    def spider_search(self, page):
        context = execjs.compile(self.js_from_file('../spider_ly/spider_ly/xxx.js'))
        cookie = self.headers.get('cookie')
        dctrack = context.call('get_dctrack', cookie)
        params = {
            "action": "getlist",
            "page": str(page),
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
        response = requests.get(self.spider_url, headers=self.headers, params=params)
        if response.status_code == 200:
            # print(response.text)
            return self.parse_search(response.text, page)

        else:
            print('出现人机验证')
            return

    def parse_search(self, text, page):
        maps = lambda x: ''.join(x).strip() if x else ''
        html = etree.HTML(text)
        if '很抱歉，没有找到' in maps(html.xpath('//p[@class="p01"]/text()')):
            print('已到最后一页')
            return 'end'
        scenery_list = html.xpath('//div[@class="scenery_list"]')
        # print(len(scenery_list))
        for i, scenery in enumerate(scenery_list):
            try:
                sid = maps(scenery.xpath('./div/div[@class="s_info"]/@sid'))
                if sid.isdigit():
                    sid = int(sid)
                detail_link = 'https:' + maps(scenery.xpath('./div/div[@class="s_info"]/a/@href'))
                main_img = 'https:' + maps(scenery.xpath('./div/div[@class="s_info"]/a/img/@src'))
                address_list = scenery.xpath('./div/div[@class="s_info"]//span[@class="sce_address"]/a/text()')
                address = ','.join(address_list)
                level = maps(scenery.xpath('./div/div[@class="s_info"]//span[@class="s_level"]/text()'))
                feature = maps(scenery.xpath('./div/div[@class="s_info"]//div[@class="info_c"]//dd[last()]/p/text()'))
                price = maps(scenery.xpath('./div/div[@class="s_info"]//div[@class="price_b"]/span/b/text()'))
                detail_text = self.get_detail_text(detail_link)
                detail_html = etree.HTML(detail_text)
                title = maps(detail_html.xpath('//h3[@class="s_name"]/text()'))
                full_address = maps(detail_html.xpath('//p[contains(@class,"s_address")]/span/text()'))
                open_time = maps(detail_html.xpath('//div[contains(@class,"s-tShow mt10")]/pre/text()')).replace('\r\n',
                                                                                                                 ' | ')
                video = maps(detail_html.xpath('//video[@id="myvideo"]/@src'))
                image_list = detail_html.xpath('//div[@class="img_s_ul"]/ul//img/@bigsrc')
                images = ['https:' + i for i in image_list]
                info_list = detail_html.xpath('//div[@class="inf-f-con"]/div')
                contents = self.get_info(info_list)
                comment_json = self.spider_comment(sid, 1)
                degreeLevel = comment_json.get('degreeLevel')
                totalNum = comment_json.get('totalNum')
                goodNum = comment_json.get('goodNum')
                midNum = comment_json.get('midNum')
                badNum = comment_json.get('badNum')
                hasImgNum = comment_json.get('hasImgNum')
                starNum = comment_json.get('starNum')
                serviceScoreAvgList = comment_json.get('serviceScoreAvgList')
                dpTagList = comment_json.get('dpTagList')
                item = [sid, title, detail_link, main_img, address, level, feature, price, full_address, open_time,
                        video, images, degreeLevel, totalNum, goodNum, midNum, badNum, hasImgNum, starNum,
                        serviceScoreAvgList,
                        dpTagList, contents]

                self.save_writer.writerow(item)
                print(f'-----第{page}页的{i + 1}入库成功-----')
                # self.save_to_csv(item)
            except:
                print(f'-----{i + 1}error-----')
        return

    def spider_comment(self, sid, page):
        url = "https://www.ly.com/scenery/AjaxHelper/DianPingAjax.aspx"
        headers = {
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
        cookies = {
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
        params = {
            "action": "GetDianPingList",
            "sid": sid,
            "page": str(page),
            "pageSize": "10",
            "labId": "1",
            "sort": "0",
            "iid": random.random()
        }
        try:
            response = requests.get(url, headers=headers, cookies=cookies, params=params)
            comment_json = response.json()
            return comment_json
            # print(f'正在抓取{sid} 第 {page}页数据！')
            # self.get_comment(sid,page, comment_json)

        except:
            print(f'{sid} 第 {page} 页有错...')

    def get_comment(self, sid, page, comment_json):
        try:
            degreeLevel = comment_json.get('degreeLevel')
            totalNum = comment_json.get('totalNum')
            goodNum = comment_json.get('goodNum')
            midNum = comment_json.get('midNum')
            badNum = comment_json.get('badNum')
            hasImgNum = comment_json.get('hasImgNum')
            starNum = comment_json.get('starNum')
            serviceScoreAvgList = comment_json.get('serviceScoreAvgList')
            dpTagList = comment_json.get('dpTagList')
            dpList = comment_json.get('dpList')

            for dp in dpList:
                comment_data = [sid, degreeLevel, totalNum, goodNum, midNum, badNum, hasImgNum, starNum,
                                serviceScoreAvgList, dpTagList]
                comment_time = dp.get('dpDate')
                comment_user = dp.get('dpUserName')
                comment_stat = dp.get('lineAccess')
                comment_cotent = dp.get('dpContent')
                csReplyList = dp.get('csReplyList')
                reply_content = csReplyList[0].get('replyContent') if csReplyList else None
                comment_data.extend([comment_time, comment_user, comment_stat, comment_cotent, reply_content])
                # print(comment_data)
                self.save_to_csv_by_comment(comment_data)
        except:
            print(f'{sid} 第 {page}页没有评论...')

    def save_to_csv_by_comment(self, data):
        with open('./comment_1.csv', 'a+', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(data)

    def get_info(self, infos):
        maps = lambda x: x[0] if x else ''
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

    def save_to_csv(self, data):
        with open('tempData_2.csv', 'a+', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(data)

    # def clear_csv(self):
    #     df = pd.read_csv('./tempData_2.csv')
    #     # 删除包含空数据的行
    #     new_df = df.dropna()
    #     # 删除重复值
    #     new_df.drop_duplicates()
    #     new_df.to_sql('movie', con=engine, index=False, if_exists='append')

    def run_data(self):
        page = int(self.get_page())
        print(f'正在爬取{page}页')
        end = self.spider_search(page)
        if end == 'end':
            return
        if page == 74:
            self.set_page(page + 1)
            return
        self.set_page(page + 1)
        self.run_data()

        # 评论
        # for i in range(1, 2):
        #     self.spider_comment('31243', i)
        # comment_data.append(comments)
        # print(comment_data)

    def run_comment(self):
        # 评论
        df = pd.read_sql('select * from travel', con=engine)
        sids = list(df['sid'].values)
        for sid in sids:
            for i in range(1, 3):
                self.spider_comment(sid, i)

    def clear_csv(self):
        # df = pd.read_csv('./comment_1.csv')
        df = pd.read_csv('./tempData_2.csv')
        # 删除包含空数据的行
        # new_df = df.dropna()
        new_df = df.fillna(value=0)
        # # 删除重复值
        new_df.drop_duplicates()
        new_df.to_sql('travel', con=engine, index=False, if_exists='append')


if __name__ == '__main__':
    spiderObj = Spider()
    # spiderObj.run_comment()
    spiderObj.run_data()
    # spiderObj.clear_csv()
