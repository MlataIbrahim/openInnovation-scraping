from typing import Iterable
import scrapy
from scrapy import Spider, Request
from ..items import GamesItem
import urllib.parse
import json
from scrapy.utils.response import response_status_message


class SteamMarketSpider(Spider):
    name = "steam"
    base = "https://steamcommunity.com/market"
    listing_url = base + "/search/render/"
    headers = {
        "Accept": "text/javascript, text/html, application/xml, text/xml, */*",
        "Accept-Language": "en-US,en;q=0.9,ar;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Referer": "https://steamcommunity.com/market/search?q=",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "X-Prototype-Version": "1.7",
        "X-Requested-With": "XMLHttpRequest",
        "sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
    }

    def start_requests(self):
        params = {
            "query": "",
            "start": 0,
            "count": 50,
            "search_descriptions": 0,
            "sort_column": "popular",
            "sort_dir": "desc",
            "norender": 1
        }
        yield Request(
            url=self.listing_url + "?" + urllib.parse.urlencode(params),
            headers=self.headers,
            callback=self.parse_listings,
            errback=self.errback_httpbin,
        )

    def parse_listings(self, response):
        if response.status == 429:
            self.logger.warning("Rate limited (429), applying delay before retrying...")
            yield Request(response.url, headers=self.headers, callback=self.parse_listings, dont_filter=True, errback=self.errback_httpbin)
            return

        try:
            data = json.loads(response.body)
        except json.JSONDecodeError:
            self.logger.error("Failed to decode JSON")
            return

        for game in data["results"]:
            item = GamesItem()
            name = game["name"]
            appid = game["asset_description"]["appid"]
            url = f"{self.base}/listings/{appid}/{name}"
            item["name"] = name
            item["sell_price"] = game.get("sale_price_text", "")
            item["sell_total_offers"] = game.get("sell_listings", 0)
            item["historical_price"] = game.get("sale_price_text", "")
            item["product_metadata"] = {
                "icon": game.get("app_icon", ""),
                "type": game["asset_description"]["type"],
                "product_url": url,
                "market": game["asset_description"].get("market_buy_country_restriction", ""),
            }
            yield item

        # Pagination
        start = data["start"] + data["pagesize"]
        total_count = data["total_count"]

        if start < total_count:
            params = {
                "query": "",
                "start": start,
                "count": 50,
                "search_descriptions": 0,
                "sort_column": "popular",
                "sort_dir": "desc",
                "norender": 1
            }
            next_page_url = self.listing_url + "?" + urllib.parse.urlencode(params)
            yield Request(
                next_page_url,
                headers=self.headers,
                callback=self.parse_listings,
                errback=self.errback_httpbin,
            )

    def errback_httpbin(self, failure):
        """Handle failed requests (network issues, HTTP errors, etc.)."""
        self.logger.error(repr(failure))

        if failure.check(scrapy.spidermiddlewares.httperror.HttpError):
            response = failure.value.response
            self.logger.error(f'HTTPError on {response.url}')
            # Retry if possible
            if response.status in [429, 500, 502, 503, 504]:
                self.logger.info(f'Retrying {response.url}')
                yield scrapy.Request(response.url, headers=self.headers, callback=self.parse_listings, dont_filter=True)

        elif failure.check(scrapy.core.downloader.handlers.http11.TunnelError):
            self.logger.error('TunnelError occurred, possible connection issue')

        else:
            self.logger.error('Other error occurred: %s', failure)


