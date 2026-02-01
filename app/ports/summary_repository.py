import pydantic
from abc import ABC, abstractmethod
from app.schemas.responses import Summary

class SummaryRepository(ABC):
    @abstractmethod
    def save(self, summary : Summary) -> None:
        pass

    @abstractmethod
    def get_by_id(self, id: str) -> Summary | None:
        pass