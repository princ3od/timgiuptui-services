from typing import Optional

from articles_matcher import match_articles
from articles_uploader import upload_articles
from logs import logger
from models import ArticlesFromCrawler


class Provider:
    def handle_crawled_data(self, data: dict) -> Optional[dict]:
        logger.info("Handling crawled data")
        articles = ArticlesFromCrawler(**data)
        match_articles(articles)
        upload_articles(articles)
