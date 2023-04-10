
from flask_caching import Cache

config = {
    'CACHE_TYPE': 'redis',  # Use Redis
    'CACHE_REDIS_HOST': '127.0.0.1',  # Host, default 'localhost'
    'CACHE_REDIS_PORT': 6379,  # Port, default 6379
    'CACHE_REDIS_DB': 1
}
# cache = Cache(app=current_app)
cache = Cache(config=config)  # 创建Cache对象