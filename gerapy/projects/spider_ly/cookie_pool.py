from concurrent.futures import ThreadPoolExecutor
import redis
import threading
from selenium import webdriver

sr = redis.Redis(db=2, host='127.0.0.1', port=6379)

maps = lambda x: x[0].decode() if x else None


def get_cookie():
    """
    获取cookie
    """
    cookies = maps(sr.lrange('cookies', 0, 0))
    if cookies:
        # print(cookies)
        sr.lpop('cookies')
        return cookies
    else:
        # run()
        get_cookie()


def run(n=100):
    """多任务启动刷cookie"""
    while 1:
        l = sr.llen('cookies')
        if l < n:
            with ThreadPoolExecutor(3) as f:
                for i in range(n - l):
                    f.submit(create_cookie_pool)


def create_cookie_pool():
    """构造cookie池"""
    driver = webdriver.PhantomJS(executable_path='/Users/zhihuanmai/opt/phantomjs-2.1.1-macosx/bin/phantomjs')
    try:
        # 指定加载页面
        driver.get("https://so.ly.com/scenery/newsearchlist_hot.aspx")
        cookie_list = driver.get_cookies()
        cookies = ''
        for l in cookie_list:
            c = l['name'] + '=' + l['value'] + '; '
            cookies += c
        print(f'{threading.current_thread().name} push cookie success')
        sr.lpush('cookies', cookies)
        driver.close()
    except:
        driver.close()
        print(f'{threading.current_thread().name} push cookie fail')


if __name__ == '__main__':
    run()
