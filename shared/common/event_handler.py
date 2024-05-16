import base64
import json

from common.constants import PROJECT_ID, PubSubTopic
from common.logs import logger
from google.cloud.pubsub_v1 import PublisherClient


def pubsub_publish(topic: PubSubTopic, data):
    publisher = PublisherClient()
    topic_path = publisher.topic_path(PROJECT_ID, topic.value)
    str_data = json.dumps(
        data,
        ensure_ascii=False,
        default=str,
        separators=(",", ":"),
    ).encode("utf-8")
    logger.info(f"Publishing to {topic_path} with data {str_data}")
    publisher.publish(topic_path, data=str_data)


def normalize_pubsub_body(body: dict):
    data = body.get("data")
    decoded_body = base64.b64decode(data).decode("utf-8")
    return json.loads(decoded_body)
