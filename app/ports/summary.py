import pydantic
from abc import ABC, abstractmethod

class Summary(ABC):
    id: str
    summary: str