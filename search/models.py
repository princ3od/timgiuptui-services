import re
from typing import Optional
from pydantic import BaseModel, root_validator
from enum import Enum

_special_chars_re = r"(\'|\"|\.|\,|\;|\<|\>|\{|\}|\[|\]|\"|\'|\=|\~|\*|\:|\#|\+|\^|\$|\@|\%|\!|\&|\)|\(|/|\-|\\)"


class SortBy(str, Enum):
    date = "date"
    relevance = "relevance"


class Order(str, Enum):
    asc = "asc"
    desc = "desc"


class Article(BaseModel):
    id: int
    title: str
    url: str
    topic: str
    source: str
    description: str
    thumbnail: str
    date: int


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
            return re.sub(_special_chars_re, " ", query)

        if "query" not in values:
            raise ValueError("query is required")
        values["query"] = _remove_special_chars(values["query"])
        if values["limit"] > 20:
            values["limit"] = 20
        return values

    def get_topic_filter(self):
        if self.topics is None or len(self.topics) == 0:
            return ""
        topics = "|".join(self.topics)
        return f"@topic:({topics})"

    def get_source_filter(self):
        if self.sources is None or len(self.sources) == 0:
            return ""
        sources = "|".join(self.sources)
        return f"@source:({sources})"

    def build_fuzzy_term(self, fuzzy_level=1):
        fuzzy_sign = "".join(["%" for _ in range(fuzzy_level)])
        fuzzy_term = "".join(
            [f"{fuzzy_sign}{word}{fuzzy_sign}" for word in self.query.split(" ")]
        )
        fuzzy_term = f"{fuzzy_term} {self.get_topic_filter()}"
        fuzzy_term = f"{fuzzy_term} {self.get_source_filter()}"
        fuzzy_term = fuzzy_term.strip()
        return fuzzy_term
