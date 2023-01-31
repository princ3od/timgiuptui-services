import os
from redis import Redis
from redis.commands.search.query import Query

from models import Article, SearchQuery, SortBy, Order

redis_client = Redis(
    host=os.environ["REDIS_HOST"],
    port=int(os.environ["REDIS_PORT"]),
    password=os.environ.get("REDIS_PASSWORD"),
)


def search_articles(search_query: SearchQuery) -> list[Article]:
    for fuzzy_level in range(1, 3):
        query = _build_query(search_query, fuzzy_level)
        result = _search(query)
        if len(result) > 0:
            return result
    return []


def _build_query(search_query: SearchQuery, fuzzy_level=1) -> Query:
    fuzzy_term = search_query.build_fuzzy_term(fuzzy_level)
    query: Query = Query(fuzzy_term)
    query = query.paging(search_query.offset, search_query.limit)
    if search_query.sort_by == SortBy.date:
        is_asc = search_query.order == Order.asc
        query = query.sort_by("date", asc=is_asc)
    return query


def _search(query: Query) -> list[Article]:
    result = redis_client.ft("articles").search(query)
    docs = sorted(result.docs, key=lambda x: x.score)
    articles = []
    for doc in docs:
        article = Article(**doc.json)
        articles.append(article)
    return articles
