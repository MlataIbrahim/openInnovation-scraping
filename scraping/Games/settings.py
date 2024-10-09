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


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "Games (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
ITEM_PIPELINES = {
    'Games.pipelines.MongoDBPipeline': 300,
}

# MongoDB connection settings
MONGO_URI = 'mongodb://mongo:27017'
MONGO_DATABASE = 'steam_market'
DOWNLOAD_DELAY = 3

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 2
AUTOTHROTTLE_MAX_DELAY = 60
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
AUTOTHROTTLE_DEBUG = True

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
