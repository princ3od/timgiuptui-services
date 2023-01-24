from typing import Optional
from models import User

from logs import logger


class Provider:
    def __init__(self):
        self.data = {}

    def get(self, id: int) -> Optional[User]:
        logger.info(f"get {id}")
        if id in self.data:
            return self.data[id]
        return None

    def create(self, model: User) -> User:
        logger.info(f"create {model}")
        self.data[model.id] = model
        return model

    def update(self, id: str, model: User) -> User:
        logger.info(f"update {id} {model}")
        self.data[id] = model
        return model

    def delete(self, id: str) -> None:
        logger.info(f"delete {id}")
        if id in self.data:
            del self.data[id]
