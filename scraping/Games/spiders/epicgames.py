import scrapy


class EpicgamesSpider(scrapy.Spider):
    name = "epicgames"
    allowed_domains = ["epic.gom"]
    start_urls = ["https://epic.gom"]

    def parse(self, response):
        pass
