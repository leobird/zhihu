# -*- coding: utf-8 -*-

# Scrapy settings for zhihu project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'zhihu'

SPIDER_MODULES = ['zhihu.spiders']
NEWSPIDER_MODULE = 'zhihu.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.2372.400 QQBrowser/9.5.10548.400'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    "Host": "www.zhihu.com",
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.2372.400 QQBrowser/9.5.10548.400",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch, br",
    "Accept-Language": "zh-CN,zh;q=0.8",
    "X-Requested-With":"XMLHttpRequest",
    "X-Xsrftoken":"335980934764f58007950f1c2ca61164",
    "Cookie":'aliyungf_tc=AQAAAD1Cn32LkQcAdNvi3QfSINibcM7m; acw_tc=AQAAALH2UyKv4gkAdNvi3fp4Y6sZlNJU; q_c1=0ce88221d3bf4edc9683abead8a6fac5|1494216456000|1494216456000; _xsrf=335980934764f58007950f1c2ca61164; r_cap_id="YjVlMGY1NjM5ZDk3NDdlMWExOGE5MDQ4OWU3YjMyZTA=|1494216456|940613c90f735800bf88786ddbec27f00deb083c"; cap_id="ZjQ4YjBmMTExZGJiNGQ5OGE4OGUzYjFlNjVlZGQxODQ=|1494216456|a7ad6f7ff5154149b5a72efffcbf8cf4c32a409a"; d_c0="AHCCeBqjuQuPTszeyQCw0R1zf3Y9BhC5CMk=|1494216457"; _zap=4bf8a890-d8ea-4f95-bec1-4b535786ce1c; l_n_c=1; __utma=51854390.858151785.1494216457.1494216457.1494225690.2; __utmb=51854390.0.10.1494225690; __utmc=51854390; __utmz=51854390.1494216457.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmv=51854390.100-1|2=registration_date=20140111=1^3=entry_date=20140111=1; z_c0=Mi4wQUFEQXplUWpBQUFBY0lKNEdxTzVDeGNBQUFCaEFsVk5UM3czV1FEaUZBQTFuaktaLVRVLU1MRXFRdi04VkxSSFFn|1494225794|4b67065a2fd2f1e76ce2e2746fc7237eb012e55c'
}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'zhihu.middlewares.ZhihuSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'zhihu.middlewares.AutoProxyMiddleware': 543,
#}

AUTO_PROXY = {
    'download_timeout': 30,
    'test_urls': [('http://upaiyun.com', 'online'), ('http://huaban.com', '33010602001878')],
    'ban_code': [500, 502, 503, 504, 400],
}
############extral
#DOWNLOADER_MIDDLEWARES =
#'scrapy_crawlera.CrawleraMiddleware': 600
#}
#CRAWLERA_ENABLED = True
#
#CRAWLERA_USER = 'leobird'
#
#CRAWLERA_PASS = '19930803'
#
#CONCURRENT_REQUESTS = 32
#
#CONCURRENT_REQUESTS_PER_DOMAIN = 32
#
#AUTOTHROTTLE_ENABLED = False
#
#DOWNLOAD_TIMEOUT = 600#
#
#CRAWLERA_PRESERVE_DELAY = True
##########
# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'zhihu.pipelines.ZhihuPipeline': 300,
}
# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5#
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'