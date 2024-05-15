from datetime import datetime
from enum import Enum
from typing import Optional

from common.logs import logger
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

    @root_validator(pre=True)
    def validate_date(cls, values):
        if "date" in values and type(values["date"]) is not str:
            try:
                values["date"] = datetime.fromtimestamp(int(values["date"])).isoformat()
            except Exception as e:
                logger.warning(f"Error parsing date: {e}")
        return values


class SearchQuery(BaseModel):
    query: str
    offset: Optional[int] = 0
    limit: Optional[int] = 10
    sort_by: Optional[SortBy] = SortBy.relevance
    order: Optional[Order] = Order.desc
    sources: Optional[list[str]] = None
    topics: Optional[list[str]] = None

    @root_validator(pre=True)
    def validate_query(cls, values):
        def _remove_special_chars(query: str) -> str:
            query = query.strip()
            while "  " in query:
                query = query.replace("  ", " ")
            return query

        if "query" not in values:
            raise ValueError("Query is required")
        values["query"] = _remove_special_chars(values["query"])
        if "limit" in values and 20 > int(values["limit"]) < 0:
            raise ValueError("Limit must be between 1 and 20")
        if "offset" in values and int(values["offset"]) < 0:
            raise ValueError("Offset must be greater than 0")
        if "sources" in values and values["sources"] is not None:
            values["sources"] = [
                _remove_special_chars(source) for source in values["sources"].split(",")
            ]
        if "topics" in values and values["topics"] is not None:
            values["topics"] = [
                _remove_special_chars(topic) for topic in values["topics"].split(",")
            ]
        return values

    def get_topic_filter(self):
        if self.topics is None or len(self.topics) == 0:
            return ""
        topics = " | ".join(self.topics)
        return f"@topic:{topics}"

    def get_source_filter(self):
        if self.sources is None or len(self.sources) == 0:
            return ""
        sources = " | ".join(self.sources)
        return f"@source:{sources}"

    def build_term(self):
        fuzzy_sign = ["%", "%%", "%%%"]
        fuzzy_terms = [self.query]
        for i in range(0, 1):
            fuzzy_words = [
                f"{fuzzy_sign[i]}{word}{fuzzy_sign[i]}"
                for word in self.query.split(" ")
            ]
            fuzzy_term = " ".join(fuzzy_words)
            fuzzy_terms.append(fuzzy_term)
        fuzzy_term = " | ".join(fuzzy_terms)
        fuzzy_term = f"{fuzzy_term} {self.get_topic_filter()}"
        fuzzy_term = f"{fuzzy_term} {self.get_source_filter()}"
        fuzzy_term = fuzzy_term.strip()
        return fuzzy_term


class SearchResult(BaseModel):
    count: int
    results: list[SimpleArticle]
    has_more: bool
