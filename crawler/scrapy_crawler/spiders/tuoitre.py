import re
from bs4 import BeautifulSoup
import scrapy
from dateutil import parser as date_parser

from scrapy_crawler.items import Article
from models import Source


class TuoiTreSpider(scrapy.Spider):
    name = "tuoitre"
    start_urls = {}
    prefix_pattern = r"(tto\s-\s)"
    download_delay = 0.01

    def __init__(self, source: Source, **kwargs):
        super().__init__(name="tuoitre", **kwargs)
        self.allowed_domains = ["tuoitre.vn"]
        self.urls_topics = source.get_urls_topics()
        self.start_urls = source.get_all_urls()

    def parse_content(self, response):
        item = response.meta["item"]
        soup = BeautifulSoup(response.body, "html.parser")
        is_magazine = soup.select_one("#contentMagazine")
        if is_magazine is not None:
            return None
        description_elem = soup.select_one("#content .detail-sapo")
        if description_elem is not None:
            item["description"] = description_elem.get_text().strip()
            item["description"] = re.sub(self.prefix_pattern, "", item["description"], 1, flags=re.IGNORECASE)
        item["author"] = soup.select_one("#content .author-info").get_text().strip()
        body_elem = soup.select_one("#content #main-detail .detail-cmain")
        item["content"] = ""
        if body_elem is not None:
            tags = body_elem.find_all("p", recursive=True)
            if len(tags) == 0:
                print(f"Warning: {item['url']} has no content [no p tag]")
            for tag in tags:
                item["content"] += tag.get_text(" ") + " \n"
        return item

    def parse(self, response):
        for rss_item in response.xpath("//channel/item"):
            item = Article()
            item["title"] = rss_item.xpath("title/text()").get()
            article_url = rss_item.xpath("link/text()").get()
            if "video" in article_url:
                continue
            item["url"] = article_url
            item["domain"] = response.url
            item["topic"] = self.urls_topics[response.url]
            item["source"] = self.name
            item["date"] = date_parser.parse(rss_item.xpath("pubDate/text()").get())
            description_raw = rss_item.xpath("description/text()").get()
            selector = scrapy.Selector(text=description_raw)
            item["thumbnail"] = selector.xpath("//img/@src").get().replace("/zoom/80_50", "")
            request = scrapy.Request(
                response.urljoin(article_url),
                callback=self.parse_content,
            )
            request.meta["item"] = item
            yield request