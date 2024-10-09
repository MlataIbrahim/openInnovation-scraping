# Scrapy settings for Games project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "Games"

SPIDER_MODULES = ["Games.spiders"]
NEWSPIDER_MODULE = "Games.spiders"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Enable Mongo pipeline
ITEM_PIPELINES = {
    'Games.pipelines.MongoDBPipeline': 300,
}

# MongoDB connection settings
MONGO_URI = 'mongodb://mongo:27017'
MONGO_DATABASE = 'steam_market'
DOWNLOAD_DELAY = 3

# Retry Handling 
RETRY_TIMES =  5
RETRY_HTTP_CODES = [429, 500, 502, 503, 504]

# Traffic Handling 
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 2
AUTOTHROTTLE_MAX_DELAY = 60
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
AUTOTHROTTLE_DEBUG = True

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
