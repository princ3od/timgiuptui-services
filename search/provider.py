from common.logs import logger
from models import Article, SearchQuery, SearchResult
from redis_search import search_articles


class Provider:
    def search(self, searh_query: SearchQuery) -> SearchResult:
        logger.info(f"Searching articles with query {searh_query}")
        articles = search_articles(searh_query)
        logger.info(f"Found {len(articles)} articles.")
        return SearchResult(
            results=articles,
            count=len(articles),
            has_more=len(articles) < searh_query.limit,
        )
