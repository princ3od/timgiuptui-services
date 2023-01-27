from enum import Enum

PROJECT_ID = "timgiuptui"


class PubSubTopicIds(Enum):
    GET_CRAWLING_SOURCES = "get-crawling-sources"
    HANDLE_ARTICLES = "handle-articles"
