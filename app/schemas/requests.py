from pydantic import BaseModel, Field, field_validator
from typing import Annotated

SummaryText = Annotated[
    str,
    Field(
        min_length = 1,
        strip_whitespace = True,
        description = "The raw text to be summarized",
        examples = ["Leadership coaching often focuses heavily on the development of ..."]
    )
]

class TextToSummary(BaseModel):
    text_to_process: SummaryText

    @field_validator("text_to_process", mode="before")
    @classmethod
    def text_not_empty(cls, v: str) -> str:
        if not v or len(v.strip()) == 0:
            raise ValueError("Text cannot be empty. Please provide content to be summarized")
        return v