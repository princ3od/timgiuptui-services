import json
from flask import Flask, Response, request
from constants import PubSubTopicIds
from models import Source
from provider import Provider

from event_handler import pubsub_publish

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
    body: dict = json.loads(request.data)
    sources = [Source(**source) for source in body]
    provider.start_crawling(sources)
    return "OK", 200