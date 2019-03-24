# -*- coding: utf-8 -*-

# Scrapy settings for news_spider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html


import logging

BOT_NAME = 'news_spider'

SPIDER_MODULES = ['news_spider.spiders']
NEWSPIDER_MODULE = 'news_spider.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'news_spider (+http://www.yourdomain.com)'

# Obey robots.txt rules
#MONGODB_CONNECTION = '/home/developMent/news_spider/news_spider/mysetting/mongodb_obj.pkl'
SIMHASH_ID = '/home/developMent/news_spider/news_spider/mysetting/simhash_obj.pkl'
PREPROCESS_CLASS = '' #预处理的类
ROBOTSTXT_OBEY = True
LOG_LEVEL = logging.INFO
LOG_STDOUT = False
LOG_FILE = "/home/developMent/data/spiderLog/spider.log" # /home/developMent
SINA_LOG_FILE = ""
LOG_FORMAT = "%(asctime)s [%(name)s] %(levelname)s: %(message)s"
SPLIT_JSON_FILE = "/home/developMent/news_spider/news_spider/mysetting/test_fenghuangwang_setting.json"
SINA_JSON_FILE = "/home/developMent/news_spider/news_spider/mysetting/sina_setting.json"
JSON_FILE = "/home/developMent/news_spider/news_spider/mysetting/json_setting_2.json"
USER_AGENT_FILE = '/home/developMent/news_spider/news_spider/mysetting/useragent.json'
#记录一般网站的错误记录
SPIDER_WRONG_FILE = "spider_wrong_file_"
#记录爬取新浪网的错误记录
SINA_LOG_FILE = '/home/developMent/data/spiderLog/sina_spider_'
GENERAL_LOG_FILE = '/home/developMent/data/spiderLog/general_spider_'
WRONG_FILE = "/home/developMent/data/wrongLog/"
SINA_WRONG_FILE = 'sina_wrong_file_'
FHW_WRONG_FILE = 'fenghuangwang_wrong_file_'
SINA_OLD_START_DATE = "1999-05-26" #新浪旧版开始时间
SINA_NEW_START_DATE = "2010-03-30" #新浪新版开始时间
SINA_MID_START_DATE = "2007-01-20" #新浪旧版的分割点（这个日期以前是用html提取链接，这个日期以后使用js）
DEPTH_LIMIT = 0
#DEPTH_STATS = True
DEPTH_STATS_VERBOSE = True
DEPTH_PRIORITY = 1 # 广度优先 scrapy调度器从LIFO变成FIFO
SCHEDULER_DISK_QUEUE = 'scrapy.squeues.PickleFifoDiskQueue'
SCHEDULER_MEMORY_QUEUE = 'scrapy.squeues.FifoMemoryQueue'
LOG_ENCODING = 'utf-8'
DOWNLOAD_TIMEOUT = 10 # 10秒-15秒之内没有下载到就退出
CONCURRENT_ITEMS = 100
CLASSIFIER_MODEL = '' #预测分类模型的位置
#CONCURRENT_REQUESTS = 4
#RETRY_ENABLED = True
#RETRY_TIME = 2
#RETRY_HTTP_CODES =[500, 502, 503, 504, 400, 408]
#DOWNLOAD_MAXSIZE = 0  #最大下载字节
#DOWNLOAD_WARNSIZE = 0 #0 disable
#MONGO_DB连接字段
#REDIRECT_MAX_TIMES = 22
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
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'news_spider.middlewares.NewsSpiderSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
#   'news_spider.middlewares.MyCustomDownloaderMiddleware': 543,
 'news_spider.middlewares.RandomUserAgent':1,
 'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware': 350,
 #'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware': 351

 }

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
 'news_spider.pipelines.PreProcessItem': 1,
 #'news_spider.pipelines.CaculateHashIDPipline':3,
 #'news_spider.pipelines.ClassifierPipline':4,
 'news_spider.pipelines.MongoDBPipline':5
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
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
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


MAIL_USER = "news_spider@sina.com"

MAIL_PASS = "zhengjianglong"

MAIL_SEND_LIST = ['840704140@qq.com']


SUBJECT = '爬虫出错'
