from constants import ARTICLES_SERVICE_URL, PLATFORM_SERVICE_URL
from fastapi import FastAPI, status
from fastapi_gateway import route
from models import (Article, Editor, Order, SearchResult, SimilarArticle,
                    SortBy, Topic)
from provider import Provider
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import Response

app = FastAPI(
    version="0.1.0",
    title="Timgiuptui API",
    description="Timgiuptui API documentation",
    swagger_ui_parameters={"displayRequestDuration": True},
)
app.add_middleware(CORSMiddleware, allow_origins=["*"])

provider = Provider()


@app.get("/", status_code=status.HTTP_200_OK)
def health():
    return "OK"


@route(
    request_method=app.get,
    service_url=ARTICLES_SERVICE_URL,
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
    service_url=ARTICLES_SERVICE_URL,
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


@route(
    request_method=app.get,
    service_url=ARTICLES_SERVICE_URL,
    gateway_path="/articles/{id}",
    service_path="/articles/{id}",
    status_code=status.HTTP_200_OK,
    tags=["Articles Service"],
    response_model=Article,
)
def get_article(request: Request, response: Response, id: str):
    pass


@route(
    request_method=app.get,
    service_url=ARTICLES_SERVICE_URL,
    gateway_path="/articles/{id}/similar",
    service_path="/articles/{id}/similar",
    status_code=status.HTTP_200_OK,
    tags=["Articles Service"],
    response_model=list[SimilarArticle],
)
def get_similar_articles_of(request: Request, response: Response, id: str):
    pass
