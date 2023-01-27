from pydantic import BaseModel


class Source(BaseModel):
    editor_id: str
    urls: dict[str, str]

    def get_urls_topics(self) -> dict[str, str]:
        urls_topics = {}
        for topic, url in self.urls.items():
            urls_topics[url] = topic
        return urls_topics

    def get_all_urls(self) -> list[str]:
        return list(self.urls.values())
