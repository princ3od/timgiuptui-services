from common.logs import logger
from models import SearchQuery
from redis_search import search_articles
from models import Article


class Provider:
    def search(searh_query: SearchQuery) -> list[Article]:
        logger.info(f"Searching articles with query {searh_query}")
        articles = search_articles(searh_query)
        logger.info(f"Found {len(articles)} articles.")
        return articles
