from fastapi import FastAPI, HTTPException, status
from models import SearchResult, SortBy, Order, Topic, Editor
from provider import Provider
from fastapi_gateway import route
from starlette.requests import Request
from starlette.responses import Response
from typing import Optional

from constants import SEARCH_SERVICE_URL, PLATFORM_SERVICE_URL

app = FastAPI(version="0.1.0", title="Timgiuptui API", description="Timgiuptui API documentation")

provider = Provider()


@app.get("/", status_code=status.HTTP_200_OK)
def health():
    return "OK"


@route(
    request_method=app.get,
    service_url=SEARCH_SERVICE_URL,
    gateway_path="/articles/search",
    service_path="/articles/search",
    query_params=["q", "offset", "limit", "sort_by", "order", "sources", "topics"],
    status_code=status.HTTP_200_OK,
    tags=["Search Service"],
    response_model=SearchResult,
)
def fulltext_search_articles(
    request: Request,
    response: Response,
    q: str,
    limit: int = 10,
    offset: int = 0,
    sort_by: SortBy = SortBy.relevance,
    order: Order = Order.desc,
    sources: str = None,
    topics: str = None,
):
    pass


@route(
    request_method=app.get,
    service_url=SEARCH_SERVICE_URL,
    gateway_path="/articles/autocomplete",
    service_path="/articles/autocomplete",
    query_params=["q"],
    status_code=status.HTTP_200_OK,
    tags=["Search Service"],
    response_model=list[str],
)
def get_autocomplete_suggestions(request: Request, response: Response, q: str):
    pass


@route(
    request_method=app.get,
    service_url=PLATFORM_SERVICE_URL,
    gateway_path="/topics",
    service_path="/topics",
    query_params=["q"],
    status_code=status.HTTP_200_OK,
    tags=["Platform Service"],
    response_model=list[Topic],
)
def get_topics(request: Request, response: Response):
    pass


@route(
    request_method=app.get,
    service_url=PLATFORM_SERVICE_URL,
    gateway_path="/editors",
    service_path="/editors",
    query_params=["q"],
    status_code=status.HTTP_200_OK,
    tags=["Platform Service"],
    response_model=list[Editor],
)
def get_sources(request: Request, response: Response):
    pass
