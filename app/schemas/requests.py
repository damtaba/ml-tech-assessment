from pydantic import BaseModel, Field, field_validator
from typing import Annotated

SummaryText = Annotated[
    str,
    Field(
        min_length = 1,
        strip_whitespace = True,
        description = "The raw text to be summarized",
        examples = ["Hi Coach, I just finished a session with Jordan. We talked for about 45 minutes. Jordan feels like they are hitting a wall with the Project Phoenix deliverables. They mentioned that the cross-functional communication with the Engineering team is 'broken' and it's causing delays. On a positive note, Jordan expressed interest in moving into a Lead role next year. I told them we’d look at the budget for a leadership certification, but first, they need to improve their delegation skills because right now they are doing everything themselves. We agreed to meet again next Tuesday to look at a revised project timeline."]
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