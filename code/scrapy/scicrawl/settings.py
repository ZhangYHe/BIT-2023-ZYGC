# Scrapy settings for scicrawl project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "scicrawl"

SPIDER_MODULES = ["scicrawl.spiders"]
NEWSPIDER_MODULE = "scicrawl.spiders"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "scicrawl (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
#HTTPERROR_ALLOWED_CODES = []#HTTP status code is not handled or not allowed的解决方法

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# 并发请求数，修改为1，或者2，越小爬取速度越慢，太快容易被识别到
# CONCURRENT_REQUESTS = 2

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# 下载延迟时间，DOWNLOAD_DELAY设置越大请求越慢
# DOWNLOAD_DELAY = 3
# #默认False;为True表示启用AUTOTHROTTLE扩展
# AUTOTHROTTLE_ENABLED = True
# #默认5秒;初始下载延迟时间
# AUTOTHROTTLE_START_DELAY = 1
# #默认60秒；在高延迟情况下最大的下载延迟
# AUTOTHROTTLE_MAX_DELAY = 3

# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "scicrawl.middlewares.ScicrawlSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   #'scicrawl.middlewares.ProxyMiddleware': 100,
   'scicrawl.middlewares.ProcessAllExceptionMiddleware': 543,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   "scicrawl.pipelines.ScicrawlPipeline": 300,
}

FILES_STORE = 'download/PDF'

# 爬虫结束条件
# CLOSESPIDER_TIMEOUT  # 指定时间退出
# CLOSESPIDER_ITEMCOUNT  # 生成了指定数量的item
# CLOSESPIDER_PAGECOUNT  # 抓取了指定数量的响应
CLOSESPIDER_ERRORCOUNT = 500  # 在发生指定数量的错误
#
# 打开EXTENSIONS扩展
EXTENSIONS = {
   'scrapy.extensions.closespider.CloseSpider': 500,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
# REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
# TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
# FEED_EXPORT_ENCODING = "utf-8"


import random
# user agent 列表
with open('utils/ua.txt', 'r', encoding='utf8') as f:
   USER_AGENT_LIST = [i.strip() for i in f]

USER_AGENT = random.choice(USER_AGENT_LIST)