# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
import pymongo

class MongoDBPipeline:

    collection_name = 'steam_market_items'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        """Pull settings from Scrapy settings."""
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'steam_market')
        )

    def open_spider(self, spider):
        """Initialize MongoDB connection when the spider starts."""
        self.client = pymongo.MongoClient(self.mongo_uri, serverSelectionTimeoutMS=10000)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        """Close MongoDB connection when the spider closes."""
        self.client.close()

    def process_item(self, item, spider):
        """Insert scraped item into MongoDB."""
        self.db[self.collection_name].insert_one(dict(item))
        return item

