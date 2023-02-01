from datetime import datetime
import re
from enum import Enum
from typing import Optional

from pydantic import BaseModel, root_validator

from common.logs import logger

_special_chars_re = r"(\'|\"|\.|\,|\;|\<|\>|\{|\}|\[|\]|\"|\'|\=|\~|\*|\:|\#|\+|\^|\$|\@|\%|\!|\&|\)|\(|/|\-|\\)"


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
    
    @root_validator(pre=True)
    def validate_query(cls, values):
        try:
            date_timestamp = values.get("date")
            values["date"] = datetime.fromtimestamp(int(date_timestamp)).isoformat()
        except Exception as e:
            logger.error(f"Error parsing date {date_timestamp}: {e}")
        return values
    


class SearchQuery(BaseModel):
    query: str
    offset: Optional[int] = 0
    limit: Optional[int] = 10
    sort_by: Optional[SortBy] = SortBy.relevance
    order: Optional[Order] = Order.desc
    sources: Optional[list[str]] = None
    topics: Optional[list[str]] = None
    is_full_text: Optional[bool] = True

    @root_validator(pre=True)
    def validate_query(cls, values):
        def _remove_special_chars(query: str) -> str:
            query = query.strip()
            while "  " in query:
                query = query.replace("  ", " ")
            return re.sub(_special_chars_re, "", query)

        if "query" not in values:
            raise ValueError("Query is required")
        values["query"] = _remove_special_chars(values["query"])
        if "limit" in values and 20 > int(values["limit"]) < 0:
            raise ValueError("Limit must be between 1 and 20")
        if "offset" in values and int(values["offset"]) < 0:
            raise ValueError("Offset must be greater than 0")
        if "sources" in values:
            values["sources"] = [_remove_special_chars(source) for source in values["sources"].split(",")]
        if "topics" in values:
            values["topics"] = [_remove_special_chars(topic) for topic in values["topics"].split(",")]
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
        if not self.is_full_text:
            return f"@title:{self.query}* {self.get_topic_filter()} {self.get_source_filter()}".strip()
        fuzzy_sign = ["%", "%%", "%%%"]
        fuzzy_terms = [self.query]
        for i in range(0, 1):
            fuzzy_words = [f"{fuzzy_sign[i]}{word}{fuzzy_sign[i]}" for word in self.query.split(" ")]
            fuzzy_term = " ".join(fuzzy_words)
            fuzzy_terms.append(fuzzy_term)
        fuzzy_term = " | ".join(fuzzy_terms)
        fuzzy_term = f"{fuzzy_term} {self.get_topic_filter()}"
        fuzzy_term = f"{fuzzy_term} {self.get_source_filter()}"
        fuzzy_term = fuzzy_term.strip()
        return fuzzy_term
