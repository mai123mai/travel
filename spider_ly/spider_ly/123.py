import requests
import json
res = requests.get('http://route.xiongmaodaili.com/xiongmao-web/api/glip?secret=35efc9dfbff51c1b980cb5780b7e8e1e&orderNo=GL202303192145360ZLUr21M&count=200&isTxt=0&proxyType=1')
f = open('ip代理_1.json','w')
json.dump(res.json(),f)