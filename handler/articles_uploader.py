import json

from constants import REDIS_EXPRIRED_TIME_IN_SECONDS
from database import firestore_db, redis_client
from datetime_normalizer import normalize_article_datetime
from logs import logger
from models import Article, ArticlesFromCrawler
from redis.commands.json.path import Path


def upload_articles(data: ArticlesFromCrawler):
    """Uploads articles to Firestore."""
    logger.info("Uploading articles to Firestore and Redis...")
    for articles in data.articles.values():
        _upload(articles)
    logger.info("Finished uploading articles to Firestore and Redis.")


def _upload(articles: list[Article]):
    for article in articles:
        logger.info(f"Uploading article {article.id} to Firestore and Redis...")
        normalize_article_datetime(article)
        _upload_firestore(article)
        _upload_redis(article)


def _upload_firestore(article: Article):
    """Uploads article to Firestore."""
    current_article_ref = firestore_db.collection("articles").document(article.id).get()
    if current_article_ref.exists:
        logger.info(f"Article {article.id} already exists in Firestore.")
        return
    firestore_db.collection("articles").document(article.id).set(article.dict())
    return True


def _upload_redis(article: Article):
    """Uploads article to Redis."""
    article_dict = json.loads(
        article.json(
            include={
                "id",
                "title",
                "url",
                "topic",
                "source",
                "description",
                "author",
                "thumbnail",
                "date",
            }
        )
    )
    result = redis_client.json().set(
        f"articles:{article.id}", Path.rootPath(), article_dict
    )
    if not result:
        logger.error(f"Failed to upload article {article.id} to Redis.")
        return result
    result = redis_client.expire(
        f"articles:{article.id}", REDIS_EXPRIRED_TIME_IN_SECONDS
    )
    return True
