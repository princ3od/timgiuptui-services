from typing import Optional

from common.logs import logger

from database import firestore_db
from models import Article, SearchQuery, SearchResult, SimilarArticle
from redis_search import search_articles, suggest_articles


class Provider:
    def get(self, id: str) -> Optional[Article]:
        logger.info(f"Getting article with id {id}")
        data = firestore_db.collection("articles").document(id).get()
        if not data.exists:
            return None
        return Article(**data.to_dict())

    def get_similar_articles_of(self, id: str) -> Optional[list[SimilarArticle]]:
        logger.info(f"Getting similar articles of article with id {id}")
        article = self.get(id)
        if article is None:
            return None
        similar_articles: list[SimilarArticle] = []
        for similar_article_id, similar_article in article.similar_articles.items():
            similar_articles.append(
                similar_article.copy(update={"id": similar_article_id})
            )
        sorted_similar_articles = sorted(
            similar_articles, key=lambda x: x.similarity, reverse=True
        )
        return sorted_similar_articles

    def search(self, searh_query: SearchQuery) -> SearchResult:
        logger.info(f"Searching articles with query {searh_query}")
        articles = search_articles(searh_query)
        logger.info(f"Found {len(articles)} articles.")
        return SearchResult(
            results=articles,
            count=len(articles),
            has_more=len(articles) == searh_query.limit,
        )

    def suggest(self, query: str) -> list[str]:
        logger.info(f"Suggesting articles with query {query}")
        suggestions = suggest_articles(query)
        logger.info(f"Found {len(suggestions)} suggestions.")
        return suggestions
