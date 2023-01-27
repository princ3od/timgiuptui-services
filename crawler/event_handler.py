import json

from constants import PROJECT_ID, PubSubTopicIds
from google.cloud.pubsub_v1 import PublisherClient
from logs import logger

try:
    publisher = PublisherClient()
except Exception as e:
    logger.error(f"Failed to initialize PublisherClient: {e}")


def pubsub_publish(topic: PubSubTopicIds, data: dict):
    topic_path = publisher.topic_path(PROJECT_ID, topic.value)
    str_data = json.dumps(data).encode("utf-8")
    publisher.publish(topic_path, data=str_data)
