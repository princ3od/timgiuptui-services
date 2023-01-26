import json
from google.cloud.pubsub_v1 import PublisherClient

from constants import PubSubTopicIds, PROJECT_ID
from database import firebase_credentials

publisher = PublisherClient(credentials=firebase_credentials)


def pubsub_publish(topic: PubSubTopicIds, data: dict):
    topic_path = publisher.topic_path(PROJECT_ID, topic.value)
    str_data = json.dumps(data).encode("utf-8")
    publisher.publish(topic_path, data=str_data)
