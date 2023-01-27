from datetime import datetime

import scrapy
from bs4 import BeautifulSoup
from models import Source
from scrapy_crawler.items import Article


class VnExpressSpider(scrapy.Spider):
    name = "vnexpress"
    start_urls = {}
    download_delay = 0

    def __init__(self, source: Source, **kwargs):
        super().__init__(name="vnexpress", **kwargs)
        self.allowed_domains = ["vnexpress.net"]
        self.urls_topics = source.get_urls_topics()
        self.start_urls = source.get_all_urls()

    def parse_content(self, response):
        item = response.meta["item"]
        soup = BeautifulSoup(response.body, "html.parser")
        item["description"] = soup.select_one("p.description").get_text(separator=" - ")
        item["author"] = soup.select_one("p.author_mail")
        if item["author"] is not None:
            item["author"] = item["author"].get_text()
        bodyElem = soup.select_one("article.fck_detail")
        item["content"] = ""
        if bodyElem is not None:
            lastP = None
            for tag in bodyElem.find_all("p"):
                if lastP == tag:
                    continue
                if self._is_content_text(tag):
                    item["content"] += tag.get_text(" ") + " \n"
                elif item["author"] is None and self._is_author_text(tag):
                    item["author"] = tag.get_text(" ")
                lastP = tag
        return item

    def parse(self, response):
        for post in response.xpath("//channel/item"):
            article_url = post.xpath("link/text()").get()
            if "video" in article_url:
                continue
            description_raw = post.xpath("description/text()").get()
            selector = scrapy.Selector(text=description_raw)
            date = datetime.strptime(
                post.xpath("pubDate/text()").get(), "%a, %d %b %Y %H:%M:%S %z"
            )
            item = Article()
            item["title"] = post.xpath("title/text()").get()
            item["url"] = article_url
            item["domain"] = response.url
            item["topic"] = self.urls_topics[response.url]
            item["source"] = self.name
            item["date"] = date
            item["thumbnail"] = selector.xpath("//img/@src").get()
            request = scrapy.Request(
                response.urljoin(article_url), callback=self.parse_content
            )
            request.meta["item"] = item
            yield request

    def _is_content_text(self, tag):
        return (
            not tag.has_attr("style")
            and not tag.has_attr("align")
            and (tag.has_attr("class") and tag["class"][0] == "Normal")
        )

    def _is_author_text(self, tag):
        return (tag.has_attr("class") and tag["class"][0] == "author") or (
            (tag.has_attr("style") and "right" in tag["style"])
            or (tag.has_attr("align") and "right" in tag["align"])
        )
