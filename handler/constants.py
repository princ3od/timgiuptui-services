from enum import Enum

LOCAL_FIRESTORE_CREDENTIAL_PATH = "crec.json"

PROJECT_ID = "timgiuptui"

FILE_PATH_VIETNAMESE_STOPWORDS = "vietnamese_stopwords.txt"

SIMILARITY_THRESHOLD = 0.85

REDIS_EXPRIRED_TIME_IN_SECONDS = 60 * 60 * 24 * 30  # 30 days


class PubSubTopicIds(Enum):
    pass
