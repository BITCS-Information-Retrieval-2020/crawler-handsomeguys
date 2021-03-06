# -*- coding: utf-8 -*-
import os
# Scrapy settings for Crossminds project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
LOCAL_MONGO_HOST = '47.103.222.126'
LOCAL_MONGO_PORT = 27017
USER_NAME = 'handsomeguys'
PASSWORD = '12138'
DB_NAME = 'crawler'

BOT_NAME = 'Crossminds'

SPIDER_MODULES = ['Crossminds.spiders']
NEWSPIDER_MODULE = 'Crossminds.spiders'

FILES_STORE = os.path.join('..', 'data', 'PDFs')
FILES_URLS_FIELD = 'file_urls'  # 这里对应着item.py文件中的字段
FILES_RESULT_FIELD = 'files'  # 同样对应item.py文件中的字段
# 120 days of delay for files expiration
FILES_EXPIRES = 120

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'Crossminds (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3
DOWNLOAD_TIMEOUT = 5000
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 15
CONCURRENT_REQUESTS_PER_IP = 15
CONCURRENT_REQUESTS = 15
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16
DEFAULT_REQUEST_HEADERS = {
    'accept': 'application/json, text/plain, */*',
    'content-type': 'application/json',
    'Connection': 'keep-alive',
    'Accept-Encoding': 'gzip, deflate, br',
    'referer': 'https://crossminds.ai/',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko)'
}
# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
    'Crossminds.middlewares.CrossmindsSpiderMiddleware': 543,
}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'Crossminds.middlewares.CrossmindsDownloaderMiddleware': 543,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
EXTENSIONS = {
    'scrapy.extensions.telnet.TelnetConsole': None,
}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'Crossminds.pipelines.CrossmindsPipeline': 300,
    'Crossminds.pipelines.PDFPipeline': 1,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
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
