import csv
import os
import random
import execjs
import requests
from lxml import etree
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('mysql+pymysql://root:123456@localhost/dbm')


class Spider():

    def __init__(self):
        self.url = "https://www.ly.com/scenery/AjaxHelper/DianPingAjax.aspx"

        self.headers = {
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
        self.cookies = {
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

    def spider_comment(self, sid, page):


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
            response = requests.get(self.url, headers=self.headers, cookies=self.cookies, params=params)
            comment_json = response.json()
            # return comment_json
            # print(f'正在抓取{sid} 第 {page}页数据！')
            self.get_comment(sid,page, comment_json)

        except:
            print(f'{sid} 第 {page} 页有错...')

    def get_comment(self, sid,page, comment_json):
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
                comment_data = [sid,degreeLevel, totalNum, goodNum, midNum, badNum, hasImgNum, starNum, serviceScoreAvgList, dpTagList]
                comment_time = dp.get('dpDate')
                comment_user= dp.get('dpUserName')
                comment_stat= dp.get('lineAccess')
                comment_cotent= dp.get('dpContent')
                csReplyList= dp.get('csReplyList')
                reply_content = csReplyList[0].get('replyContent') if csReplyList else None
                comment_data.extend([comment_time,comment_user,comment_stat,comment_cotent,reply_content])
                # print(comment_data)
                self.save_to_csv_by_comment(comment_data)
        except:
            print(f'{sid} 第 {page}页没有评论...')

    def save_to_csv_by_comment(self,data):
        with open('./comment_1.csv', 'a+', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(data)

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
    spiderObj.run_comment()
    # spiderObj.run_data()
    # spiderObj.clear_csv()
