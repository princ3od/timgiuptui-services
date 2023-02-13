from fastapi import FastAPI, HTTPException, status
from models import (Article, Order, SearchQuery, SearchResult, SimilarArticle,
                    SortBy)
from provider import Provider

app = FastAPI(version="0.1.0", title="FastAPI", description="FastAPI example")

provider = Provider()


@app.get("/", status_code=status.HTTP_200_OK)
def health():
    return "OK"


@app.get(
    "/articles/search", status_code=status.HTTP_200_OK, response_model=SearchResult
)
def fulltext_search_articles(
    q: str,
    limit: int = 10,
    offset: int = 0,
    sort_by: SortBy = SortBy.relevance,
    order: Order = Order.desc,
    sources: str = None,
    topics: str = None,
):
    try:
        q = SearchQuery(
            query=q,
            limit=limit,
            offset=offset,
            sort_by=sort_by,
            order=order,
            sources=sources,
            topics=topics,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    result = provider.search(q)
    return result


@app.get(
    "/articles/autocomplete", status_code=status.HTTP_200_OK, response_model=list[str]
)
def get_autocomplete_suggestions(q: str):
    return provider.suggest(q)


@app.get("/articles/{id}", status_code=status.HTTP_200_OK, response_model=Article)
def get_article(id: str):
    article = provider.get(id)
    if article is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Article not found"
        )
    return article


@app.get(
    "/articles/{id}/similar",
    status_code=status.HTTP_200_OK,
    response_model=list[SimilarArticle],
)
def get_article(id: str):
    similar_articles = provider.get_similar_articles_of(id)
    if similar_articles is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Article not found"
        )
    return similar_articles
