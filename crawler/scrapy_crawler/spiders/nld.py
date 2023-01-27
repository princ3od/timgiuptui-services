import re

import scrapy
from bs4 import BeautifulSoup
from dateutil import parser as date_parser
from models import Source
from scrapy_crawler.items import Article


class NguoiLaoDongSpider(scrapy.Spider):
    start_urls = []
    name = "nld"
    download_delay = 0
    prefix_pattern = r"((\(NLĐO\))\s*(–|-)\s*)"

    def __init__(self, source: Source, **kwargs):
        super().__init__(name="nld", **kwargs)
        self.allowed_domains = ["nld.com.vn"]
        self.urls_topics = source.get_urls_topics()
        self.start_urls = source.get_all_urls()
        print(self.start_urls)
        print(self.urls_topics)

    def parse_content(self, response):
        item = response.meta["item"]
        soup = BeautifulSoup(response.body, "html.parser")
        item["description"] = (
            soup.select_one(".sapo-detail").get_text(separator=" - ").strip()
        )
        item["description"] = re.sub(
            self.prefix_pattern, "", item["description"], 1, flags=re.IGNORECASE
        )
        item["author"] = soup.select_one(".author.fr").get_text().strip()
        bodyElem = soup.select_one(".content-news-detail.old-news")
        item["content"] = ""
        if bodyElem is not None:
            for tag in bodyElem.find_all("p", recursive=False):
                item["content"] += tag.get_text(" ") + " \n"
        item["content"] = item["content"].strip()
        return item

    def parse(self, response):
        for rss_item in response.xpath("//channel/item"):
            item = Article()
            item["title"] = rss_item.xpath("title/text()").get().strip()
            article_url = rss_item.xpath("link/text()").get().strip()
            if "video" in article_url:
                continue
            item["url"] = article_url
            item["domain"] = response.url
            item["topic"] = self.urls_topics[response.url]
            item["source"] = self.name
            item["date"] = date_parser.parse(rss_item.xpath("pubDate/text()").get())
            description_raw = rss_item.xpath("description/text()").get()
            selector = scrapy.Selector(text=description_raw)
            item["thumbnail"] = selector.xpath("//img/@src").get()
            request = scrapy.Request(
                response.urljoin(article_url),
                callback=self.parse_content,
            )
            request.meta["item"] = item
            yield request
