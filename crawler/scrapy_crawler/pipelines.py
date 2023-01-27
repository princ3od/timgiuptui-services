import json
import timeit
from datetime import datetime

from slugify import slugify

from logs import logger


class NewsCrawlerPipeline:
    articles_by_topics: dict[str, dict] = {}
    save_spider_articles = False

    def process_item(self, item, spider):
        if item["author"] is None:
            item["author"] = ""
        else:
            item["author"] = item["author"].replace("\n", "").strip()
        id_parts = [item["title"], spider.name, item["date"].strftime("%d-%m")]
        item["id"] = slugify(" ".join(id_parts))
        _item = {
            "id": item["id"],
            "title": item["title"],
            "url": item["url"],
            "domain": item["domain"],
            "topic": item["topic"],
            "source": item["source"],
            "description": item["description"],
            "content": item["content"],
            "author": item["author"],
            "date": item["date"],
            "thumbnail": item["thumbnail"],
            "accessed_date": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S %z"),
        }
        self._store_article(_item)
        return item

    def open_spider(self, spider):
        self.spider_articles = {}
        self.start_time = timeit.default_timer()
        logger.info(f"> Start crawling {spider.name}...")

    def close_spider(self, spider):
        if self.save_spider_articles:
            with open(f"{spider.name}.json", "w", encoding="utf-8") as file:
                json.dump(
                    self.spider_articles,
                    file,
                    ensure_ascii=False,
                    indent=2,
                    default=str,
                )
        elapsed_time = round(timeit.default_timer() - self.start_time, 4)
        logger.info(f">> Time elapsed for {spider.name}: {elapsed_time}s")

    def _store_article(self, item):
        topic = item["topic"]
        logger.info(f"> {topic}: {item['title']}")
        if topic not in self.articles_by_topics:
            self.articles_by_topics[topic] = {}
        if topic not in self.spider_articles:
            self.spider_articles[topic] = {}
        self.articles_by_topics[topic][item["id"]] = item
        self.spider_articles[topic][item["id"]] = item
