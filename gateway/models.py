from enum import Enum

from pydantic import BaseModel


class SortBy(str, Enum):
    date = "date"
    relevance = "relevance"


class Order(str, Enum):
    asc = "asc"
    desc = "desc"


class Article(BaseModel):
    id: str
    title: str
    url: str
    topic: str
    source: str
    description: str
    thumbnail: str
    date: str


class SearchResult(BaseModel):
    count: int
    results: list[Article]
    has_more: bool


class Topic(BaseModel):
    id: str
    ordinal: int
    name: str


class Editor(BaseModel):
    id: str
    name: str
    logo: str
    slogan: str
