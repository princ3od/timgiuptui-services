from enum import Enum

LOCAL_FIRESTORE_CREDENTIAL_PATH = "crec.json"
PROJECT_ID = "timgiuptui"


class PubSubTopic(Enum):
    GET_CRAWLING_SOURCES = "get-crawling-sources"
    HANDLE_ARTICLES = "handle-articles"
    INITIALIZE_CRAWLER = "initialize-crawler"
    START_CRAWLING = "start-crawling"
