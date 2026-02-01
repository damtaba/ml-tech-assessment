from pydantic import BaseModel

class SummaryLLMOutput(BaseModel):
    content: str
    ctas: list[str]