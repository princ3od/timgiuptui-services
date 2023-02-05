from typing import Optional

from common.logs import logger
from database import firestore_db
from models import Article, SimilarArticle


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
