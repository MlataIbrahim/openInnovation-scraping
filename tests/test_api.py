from fastapi.testclient import TestClient
from unittest.mock import patch
from app.app import app  # Ensure the correct path is imported
import unittest
client = TestClient(app)

class TestAPI(unittest.TestCase):

    @patch('pymongo.MongoClient')
    def test_get_products_no_data(self, mock_mongo_client):
        mock_db = mock_mongo_client.return_value['steam_market']
        mock_db.steam_market_items.find.return_value = []
        mock_db.steam_market_items.count_documents.return_value = 0

        response = client.get("/products/")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "No products found"})

    @patch('pymongo.MongoClient')
    def test_get_products_with_data(self, mock_mongo_client):
        mock_db = mock_mongo_client.return_value['steam_market']

        mock_db.steam_market_items.find.return_value = [
            {"_id": "1", "name": "Test Product", "price": "10.99"}
        ]
        mock_db.steam_market_items.count_documents.return_value = 1

        response = client.get("/products/")

        self.assertEqual(response.status_code, 200)
        expected_response = {
            "offset": 0,
            "limit": 10,
            "total": 1,
            "products": [{"_id": "1", "name": "Test Product", "price": "10.99"}]
        }
        self.assertEqual(response.json(), expected_response)

if __name__ == "__main__":
    unittest.main()
