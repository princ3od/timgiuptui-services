import json

from common.logs import logger
from constants import REDIS_EXPRIRED_TIME_IN_SECONDS
from database import firestore_db, redis_client
from datetime_normalizer import normalize_article_datetime
from models import Article, ArticlesFromCrawler
from redis.commands.json.path import Path
from redis.commands.search.suggestion import Suggestion


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
    firestore_db.collection("articles").document(article.id).set(
        article.dict(), merge=True
    )
    return True


def _upload_redis(article: Article):
    """Uploads article to Redis."""
    article_dict = json.loads(
        article.json(
            include={
                "id",
                "title",
                "topic",
                "source",
                "description",
                "thumbnail",
                "date",
                "url",
            }
        )
    )
    result = redis_client.json().set(
        f"articles:{article.id}", Path.rootPath(), article_dict
    )
    if not result:
        logger.error(f"Failed to upload article {article.id} to Redis.")
        return result
    result = redis_client.ft("articles").sugadd(
        "articles", Suggestion(string=article.title, score=article_dict["date"])
    )
    if not result:
        logger.error(f"Failed to add suggestion for article {article.id} to Redis.")
        return result
    redis_client.expire(f"articles:{article.id}", REDIS_EXPRIRED_TIME_IN_SECONDS)
    return True
