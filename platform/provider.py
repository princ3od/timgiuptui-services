from database import firestore_db
from logs import logger
from models import Editor, Source, Topic


class Provider:
    def __init__(self):
        self.data = {}

    def get_topics(self) -> list[Topic]:
        logger.info("Getting topics")
        data: dict = (
            firestore_db.collection("topics").document("content").get().to_dict()
        )
        topics: list[Topic] = []
        for topic_id, topic in data.items():
            topic["id"] = topic_id
            topics.append(Topic(**topic))
        topics = sorted(topics, key=lambda topic: topic.ordinal)
        return topics

    def get_editors(self) -> list[Editor]:
        logger.info("Getting editors")
        data: dict = (
            firestore_db.collection("editors").document("content").get().to_dict()
        )
        editors = []
        for editor_id, editor in data.items():
            editor["id"] = editor_id
            editors.append(Editor(**editor))
        return editors

    def get_sources(self) -> list[Source]:
        logger.info("Getting sources")
        data: dict = (
            firestore_db.collection("sources").document("content").get().to_dict()
        )
        sources = []
        for editor_id, source in data.items():
            source["editor_id"] = editor_id
            sources.append(Source(**source))
        return sources
