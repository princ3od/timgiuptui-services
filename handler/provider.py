from typing import Optional

from models import ArticlesFromCrawler
from logs import logger
from articles_matcher import match_articles
from articles_uploader import upload_articles


class Provider:
    def handle_crawled_data(self, data: dict) -> Optional[dict]:
        logger.info("Handling crawled data")
        articles = ArticlesFromCrawler(**data)
        match_articles(articles)
        upload_articles(articles)
