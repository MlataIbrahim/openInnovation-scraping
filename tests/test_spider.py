import unittest
from scraping.Games.spiders.steam import SteamMarketSpider
from scrapy.http import HtmlResponse, Request
import json

class TestSteamMarketSpider(unittest.TestCase):

    def setUp(self):
        self.spider = SteamMarketSpider()

    def test_start_requests(self):
        start_requests = list(self.spider.start_requests())
        self.assertEqual(len(start_requests), 1)
        self.assertTrue(start_requests[0].url.startswith("https://steamcommunity.com/market/search/render"))

    def test_parse_listings(self):
        request = Request(url="https://steamcommunity.com/market/search/render/")
        body = json.dumps({
            "start": 0,
            "pagesize": 100,
            "total_count": 1,
            "results": [
                {
                    "name": "Test Game Without Price",
                    "sell_listings": 50,
                    "asset_description": {
                        "appid": "54321",
                        "type": "game"
                    }
                }
            ]
        }).encode('utf-8')
        response = HtmlResponse(url=request.url, body=body, request=request)
        parsed_items = list(self.spider.parse_listings(response))
        self.assertEqual(len(parsed_items), 1)
        self.assertEqual(parsed_items[0]["name"], "Test Game Without Price")

if __name__ == "__main__":
    unittest.main()
