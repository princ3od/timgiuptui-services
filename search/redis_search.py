import json
import os

from common.logs import logger
from models import Article, Order, SearchQuery, SortBy
from redis import ConnectionPool, Redis
from redis.commands.search.query import Query

connection_pool = ConnectionPool(
    host=os.environ["REDIS_HOST"],
    port=int(os.environ["REDIS_PORT"]),
    password=os.environ.get("REDIS_PASSWORD"),
)

redis_client = Redis(connection_pool=connection_pool, socket_timeout=30)


def search_articles(search_query: SearchQuery) -> list[Article]:
    query = _build_query(search_query)
    result = _search(query)
    return result


def suggest_articles(query: str) -> list[str]:
    results = redis_client.ft("articles").sugget("articles", query, fuzzy=len(query) > 3, num=8)
    return results


def _build_query(search_query: SearchQuery) -> Query:
    term = search_query.build_term()
    logger.info(f"Searching articles with term {term}")
    query: Query = Query(term).with_scores()
    query = query.highlight(tags=["<b>", "</b>"])
    query = query.paging(search_query.offset, search_query.limit)
    if search_query.sort_by == SortBy.date:
        is_asc = search_query.order == Order.asc
        query = query.sort_by("date", asc=is_asc)
    return query


def _search(query: Query) -> list[Article]:
    result = redis_client.ft("articles").search(query)
    docs = result.docs
    articles = []
    for doc in docs:
        article = Article(**json.loads(doc.json))
        articles.append(article)
        logger.info(f'Found article "{article.title}" with score {doc.score}')
    return articles
