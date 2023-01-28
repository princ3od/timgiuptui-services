from pydantic import BaseModel, root_validator


class Topic(BaseModel):
    id: str
    ordinal: int
    name: str
    url: str


class Editor(BaseModel):
    id: str
    name: str
    logo: str
    slogan: str


class Source(BaseModel):
    editor_id: str
    urls: dict[str, str]

    @root_validator(pre=True)
    def generate_urls(cls, values: dict[str, str]):
        non_topic_fields = ["editor_id", "urls"]
        values["urls"] = {}
        for field_name, field_value in values.items():
            if field_name in non_topic_fields:
                continue
            values["urls"][field_name] = field_value["url"]
        return values
