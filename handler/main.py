from common.event_handler import normalize_pubsub_body
from flask import Flask, request
from provider import Provider

app = Flask(__name__)

provider = Provider()


@app.get("/")
def health():
    return "OK", 200


@app.post("/crawler/handle")
def handler_crawled_data():
    envelop = request.get_json()
    if envelop is None or envelop.get("message") is None:
        return "No body", 400
    data = normalize_pubsub_body(envelop["message"])
    provider.handle_crawled_data(data)
    return "OK", 200
