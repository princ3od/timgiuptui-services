from fastapi import FastAPI, HTTPException, status
from models import Order, SearchQuery, SearchResult, SortBy
from starlette.middleware.cors import CORSMiddleware
from provider import Provider

app = FastAPI(
    version="0.1.0",
    title="[timgiuptui] Search Service",
    description="Search service documentation",
    swagger_ui_parameters={"displayRequestDuration": True},
)
app.add_middleware(CORSMiddleware, allow_origins=["*"])

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
