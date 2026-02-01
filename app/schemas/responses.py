from pydantic import BaseModel
from app.domain.entities import Summary

class SummaryResponse(BaseModel):
    id: str
    summary: str
    ctas: list[str]

    @classmethod
    def from_entity(cls, entity: Summary):
        return cls(
            id = entity.id,
            summary = entity.content,
            ctas=entity.ctas
        )