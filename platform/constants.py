from enum import Enum

LOCAL_FIRESTORE_CREDENTIAL_PATH = "crec.json"
LOCAL_GCP_CREDENTIAL_PATH = "gcp.json"

PROJECT_ID = "timgiuptui"


class PubSubTopicIds(Enum):
    START_CRAWLING = "start-crawling"
