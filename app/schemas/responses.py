from pydantic import BaseModel

class Summary(BaseModel):
    id: str
    summary: str
    ctas: list[str]