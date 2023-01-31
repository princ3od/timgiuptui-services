import datetime
from typing import Optional, Union

from common.logs import logger
from pydantic import BaseModel, root_validator


class Article(BaseModel):
    id: str
    title: str
    url: str
    domain: str
    topic: str
    source: str
    description: str
    content: str
    author: str
    date: Union[str, datetime.datetime]
    accessed_date: Union[str, datetime.datetime]
    thumbnail: str
    similar_articles: Optional[dict[str, dict[str, dict]]] = {}
    read_time_minutes: Optional[int]

    def get_full_text(self):
        return f"{self.title}. {self.description} {self.content}"

    class Config:
        json_encoders = {datetime.datetime: lambda v: v.timestamp()}


class ArticlesFromCrawler(BaseModel):
    articles: dict[str, list[Article]]

    @root_validator(pre=True)
    def validate(cls, values: dict[str, list[dict]]):
        non_topic_fields = ["articles"]
        values["articles"] = {}
        for topic_id, articles in values.items():
            if topic_id in non_topic_fields:
                continue
            values["articles"][topic_id] = []
            for article in articles.values():
                try:
                    values["articles"][topic_id].append(Article(**article))
                except Exception as e:
                    logger.error(f"Failed to parse article: {e}")
        return values
