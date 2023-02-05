from enum import Enum
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, root_validator


class SortBy(str, Enum):
    date = "date"
    relevance = "relevance"


class Order(str, Enum):
    asc = "asc"
    desc = "desc"


class SimpleArticle(BaseModel):
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
    results: list[SimpleArticle]
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


class SimilarArticle(BaseModel):
    id: Optional[str]
    title: str
    url: str
    thumbnail: str
    source: str
    similarity: float


class Article(BaseModel):
    id: str
    accessed_date: datetime
    author: str
    content: str
    date: datetime
    description: str
    domain: str
    read_time_minutes: int
    source: str
    thumbnail: str
    title: str
    topic: str
    url: str
    similar_articles: dict[str, SimilarArticle]

    @root_validator(pre=True)
    def validate_similar_articles(cls, values):
        similar_articles = values.get("similar_articles")
        if similar_articles:
            values["similar_articles"] = {k: SimilarArticle(**v) for k, v in similar_articles.items()}
        return values

    class Config:
        json_encoders = {
            datetime: lambda dt: dt.isoformat(),
        }
