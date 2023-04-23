# Scrapy settings for spider_ly project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'spider_ly'

SPIDER_MODULES = ['spider_ly.spiders']
NEWSPIDER_MODULE = 'spider_ly.spiders'

DATA_CONFIG = {
    'config': {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'password': '123456',
        'db': 'dbm',
        'charset': 'utf8mb4'
    }
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'spider_ly (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# 调度
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# 请求指纹去重
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# redis 下发任务
REDIS_URL = 'redis://127.0.0.1:6379/1'
# 任务获取顺序
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.PriorityQueue'
# 如果不想自动清空爬取队列和去重指纹集合，可以增加如下配置
SCHEDULER_PERSIST = True
# DOWNLOAD_TIMEOUT = 2000
RETRY_TIMES = 5

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 24
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#     'spider_ly.middlewares.SpiderLySpiderMiddleware': 543,
# }
LOG_LEVEL = 'ERROR'  # 配置日志为警告级别，如果有数据是警告级别那么将记录到文件
LOG_FILE = '../log/erro.log'
# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    # 'spider_ly.middlewares.UAMiddleware': 543,
    'spider_ly.middlewares.ProxyMiddleWare': 500,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    # 'spider_ly.pipelines.SpiderLyPipeline': 210,
    # 'spider_ly.pipelines.saveCsvScrapyPipeline': 200,
    'spider_ly.pipelines.saveMysqlScrapyPipeline': 300,
    'scrapy_redis.pipelines.RedisPipeline': 310,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
import logging
from loguru import logger


# 添加 InterceptHandler() 类
class InterceptHandler(logging.Handler):
    def emit(self, record):
        # ✓ corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


# 使用 InterceptHandler() 类
logging.basicConfig(handlers=[InterceptHandler()], level=0)

# 添加
logger.add("../log/crawl_scenic_{time}.log", level="INFO", rotation="10 MB")
