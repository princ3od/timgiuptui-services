from common.logs import logger
from models import Article, SearchQuery
from redis_search import search_articles


class Provider:
    def search(self, searh_query: SearchQuery) -> list[Article]:
        logger.info(f"Searching articles with query {searh_query}")
        articles = search_articles(searh_query)
        logger.info(f"Found {len(articles)} articles.")
        return {
            "count": len(articles),
            "results": articles,
            "has_more": False if len(articles) < searh_query.limit else True,
        }
