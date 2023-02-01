from fastapi import FastAPI, HTTPException, status
from models import Order, SearchQuery, SortBy, Article, SearchResult
from provider import Provider

app = FastAPI(
    version="0.1.0",
    title="[timgiuptui] Search Service",
    description="Search service documentation",
    swagger_ui_parameters={"displayRequestDuration": True},
)
provider = Provider()


@app.get("/", status_code=status.HTTP_200_OK)
def health():
    return "OK"


@app.get("/articles/search", status_code=status.HTTP_200_OK, response_model=SearchResult)
def fulltext_search_articles(
    query: str,
    limit: int = 10,
    offset: int = 0,
    sort_by: SortBy = SortBy.relevance,
    order: Order = Order.desc,
    sources: str = None,
    topics: str = None,
):
    try:
        query = SearchQuery(
            query=query,
            limit=limit,
            offset=offset,
            sort_by=sort_by,
            order=order,
            sources=sources,
            topics=topics,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    result = provider.search(query)
    return result


@app.get("/articles/autocomplete", status_code=status.HTTP_200_OK, response_model=list[Article])
def get_autocomplete_suggestions(query: str):
    try:
        query = SearchQuery(query=query, is_full_text=False, limit=8)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    result: SearchResult = provider.search(query)
    return result.results
