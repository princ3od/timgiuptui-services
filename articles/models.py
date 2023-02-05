from datetime import datetime
from typing import Optional

from pydantic import BaseModel, root_validator


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
            values["similar_articles"] = {
                k: SimilarArticle(**v) for k, v in similar_articles.items()
            }
        return values

    class Config:
        json_encoders = {
            datetime: lambda dt: dt.isoformat(),
        }
