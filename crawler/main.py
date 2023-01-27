from constants import PubSubTopicIds
from event_handler import normalize_pubsub_body, pubsub_publish
from flask import Flask, request
from models import Source
from provider import Provider

app = Flask(__name__)

provider = Provider()


@app.get("/")
def health():
    return "OK", 200


@app.post("/crawler/initialize")
def init_crawler():
    pubsub_publish(topic=PubSubTopicIds.GET_CRAWLING_SOURCES, data={})
    return "OK", 200


@app.post("/crawler/start")
def start_crawler():
    body: list = normalize_pubsub_body(request.get_json())
    sources = [Source(**source) for source in body]
    provider.start_crawling(sources)
    return "OK", 200
