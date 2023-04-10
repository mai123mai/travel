import execjs
import requests

#
#
headers = {
    "authority": "www.evans.co.uk",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "sec-ch-ua": "\"Chromium\";v=\"110\", \"Not A(Brand\";v=\"24\", \"Google Chrome\";v=\"110\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"macOS\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}
cookies = {
    "_sp_ses.0dc5": "*",
    "__cf_bm": "JVFcbz2jqMKnxZWSnAEkprcVXlYKCFenIbU9GSFCRNU-1677728761-0-AYRRG/XTp37ktA8MzcvbRZPjyU6506GfOI3fFx+msVOP+jb3zWE50xFbkg+URiTsl5lebscIEETinuUlo9H+7zY=",
    "mage-cache-storage": "%7B%7D",
    "mage-cache-storage-section-invalidation": "%7B%7D",
    "nostojs": "autoload",
    "notice_gdpr_prefs": "0|1|2:",
    "notice_preferences": "2:",
    "2c.cId": "64001c0cf42b087e4e435483",
    "yotpo_pixel": "81cfc3a6-1b4b-474d-b1e8-3de7ff987298",
    "_sp_id.0dc5": "043b9f8080d07958.1677728761.1.1677728797.1677728761"
}
url = "https://www.evans.co.uk/naomi-maxi-dress-navy"
params = {
    "catfilter": "eyJpZCI6IjExMjIxIn0="
}
response = requests.get(url, headers=headers, cookies=cookies, params=params)
proxys = {
    'http': 'http://proxy.ym:5500',
    # 'https': 'https://proxy.ym:5500',
}
# print(response.cookies)
# cf_bm = dict(response.cookies).get('__cf_bm')
# print(cookies)
# cookies['__cf_bm'] = cf_bm
# print(cookies)
# res = requests.get(url, headers=headers, cookies=cookies, params=params, proxies=proxys)
# print(res)
# # print(res.text)
#
# # pip install cloudscraper
# target_url = 'https://www.evans.co.uk/naomi-maxi-dress-navy?catfilter=eyJpZCI6IjExMjIxIn0%3D'
# import cfscrape
# # 实例化一个create_scraper对象
# scraper = cfscrape.create_scraper()
# # 请求报错，可以加上时延
# # scraper = cfscrape.create_scraper(delay = 10)
# # 获取网页源代码
# web_data = scraper.get(target_url).content
# print(web_data)


def js_from_file(file_name):
    with open(file_name, 'r', encoding='UTF-8') as file:
        result = file.read()
    return result


def spider_search():
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Referer": "https://www.ly.com/",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        "sec-ch-ua": "\"Chromium\";v=\"110\", \"Not A(Brand\";v=\"24\", \"Google Chrome\";v=\"110\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"macOS\"",
        'cookie': 'NewProvinceId=6; NCid=91; NewProvinceName=%E5%B9%BF%E4%B8%9C; NCName=%E6%B7%B1%E5%9C%B3; __tctmu=144323752.0.0; longKey=167696968473806; __tctrack=0; Hm_lvt_64941895c0a12a3bdeb5b07863a52466=1676969694,1677573749; H5CookieId=1fca5a4e-75aa-44cd-bf37-3966c655038c; Hm_lvt_c6a93e2a75a5b1ef9fb5d4553a2226e5=1677573758; dj-meta=%257B%2522ttf%2522%3A%252211011010110111110001001101111100010110011111000%257C1011011110000001101000%2522%2C%2522tz%2522%3A-480%2C%2522au%2522%3A%252248000_2_1_0_2_explicit_speakers%2522%2C%2522gp%2522%3A%2522Google%2520Inc.%2520(Intel%2520Inc.)%40ANGLE%2520(Intel%2520Inc.%2C%2520Intel(R)%2520Iris(TM)%2520Plus%2520Graphics%2520OpenGL%2520Engine%2C%2520OpenGL%25204.1)%2522%2C%2522cv%2522%3A%25222d58a52d428e99d1e377c9376b06732049d1ef27%2522%2C%2522pls%2522%3A%2522PDF%2520ViewerChrome%2520PDF%2520ViewerChromium%2520PDF%2520ViewerMicrosoft%2520Edge%2520PDF%2520ViewerWebKit%2520builtin%2520PDF%2522%2C%2522hd%2522%3A%2522zh-CN_zh_8%2522%2C%2522sc%2522%3A%2522900_1440_30_2%2522%2C%2522ua%2522%3A%2522Mozilla%2F5.0%2520(Macintosh%3B%2520Intel%2520Mac%2520OS%2520X%252010_15_7)%2520AppleWebKit%2F537.36%2520(KHTML%2C%2520like%2520Gecko)%2520Chrome%2F110.0.0.0%2520Safari%2F537.36%2522%2C%2522ft%2522%3A%25229ed34b46ca3c1706db122622a6685455e3f082e7%2522%2C%2522lg%2522%3A%25224a95d43fd6e3dc68abc0444e278484fc8432c22c%2522%257D; _ga=GA1.2.605122596.1677573761; __tctmz=144323752.1677652965859.3.2.utmccn=(referral)|utmcsr=google.com|utmcct=|utmcmd=referral; udc_feedback=%7B%22url%22%3A%20%22https%3A%2F%2Fgny.ly.com%2F%22%2C%22platform%22%3A%20%22PC%22%2C%22channel%22%3A%20%22%E5%9B%BD%E5%86%85%E6%B8%B8%22%2C%22page%22%3A%20%22%E5%9B%BD%E5%86%85%E8%AF%A6%E6%83%85%E9%A1%B5%22%7D; pt__search_from=channel=scenery&page=scenery-index; wwwscenery=e63385c94ba81a32d30bcedf71ec319f; ASP.NET_SessionId=cyyrd3b1z5x2delfmt1bdcwa; pagestate=1; Hm_lpvt_64941895c0a12a3bdeb5b07863a52466=1677657686; qdid=28045|1|14211829|40699c,28045|1|14211829|40699c,28045|1|14211829|40699c; __tctma=144323752.167696968473806.1676969684373.1677657690291.1677736163929.5; __tccgd=144323752.0; Hm_lpvt_c6a93e2a75a5b1ef9fb5d4553a2226e5=1677748333; indexTopSearchHistory=%5B%22%E4%BA%91%E5%8D%97%22%2C%22%E5%B9%BF%E4%B8%9C%22%2C%22%E5%9B%9B%E5%B7%9D%22%2C%22%E5%8E%A6%E9%97%A8%22%5D; 17uCNRefId=RefId=14211829&SEFrom=so&SEKeyWords=%E5%B9%BF%E4%B8%9C; TicketSEInfo=RefId=14211829&SEFrom=so&SEKeyWords=%E5%B9%BF%E4%B8%9C; CNSEInfo=RefId=14211829&tcbdkeyid=&SEFrom=so&SEKeyWords=%E5%B9%BF%E4%B8%9C&RefUrl=https%3A%2F%2Fso.ly.com%2Fscenery%3Fq%3D%25E5%25B9%25BF%25E4%25B8%259C; __tctmc=144323752.32486332; __tctmd=144323752.134765555; __tctmb=144323752.220804471399657.1677748385142.1677748503823.4'
    }
    context = execjs.compile(js_from_file('xxx.js'))
    cookie = headers.get('cookie')
    dctrack = context.call('get_dctrack', cookie)
    print(dctrack)

spider_search()