import unittest
from unittest.mock import patch, MagicMock
from scraping.Games.pipelines import MongoDBPipeline

class TestMongoDBPipeline(unittest.TestCase):

    def setUp(self):
        """Set up the MongoDBPipeline instance for testing."""
        self.mongo_uri = 'mongodb://localhost:27017'
        self.mongo_db = 'steam_market'
        self.pipeline = MongoDBPipeline(self.mongo_uri, self.mongo_db)

    @patch('pymongo.MongoClient')
    def test_open_spider(self, mock_mongo_client):
        pipeline = MongoDBPipeline(mongo_uri="mongodb://localhost:27017", mongo_db="steam_market")
        spider = None
        pipeline.open_spider(spider)
        mock_mongo_client.assert_called_once()

    @patch('scraping.Games.pipelines.pymongo.MongoClient')
    def test_close_spider(self, mock_mongo_client):
        """Test that the MongoDB connection is closed when the spider closes."""
        spider = MagicMock()
        self.pipeline.open_spider(spider)
        
        self.pipeline.close_spider(spider)
        
        self.pipeline.client.close.assert_called_once()

    @patch('scraping.Games.pipelines.pymongo.MongoClient')
    def test_process_item(self, mock_mongo_client):
        """Test that items are correctly inserted into MongoDB."""
        spider = MagicMock()
        self.pipeline.open_spider(spider)

        item = {
            'name': 'Test Game',
            'sell_price': '$9.99',
            'sell_total_offers': 100,
            'historical_price': '$9.99',
            'product_metadata': {
                'icon': 'icon_url',
                'type': 'game',
                'product_url': 'url',
                'market': 'N/A'
            }
        }

        self.pipeline.process_item(item, spider)
        
        self.pipeline.db[self.pipeline.collection_name].insert_one.assert_called_once_with(item)

if __name__ == '__main__':
    unittest.main()
