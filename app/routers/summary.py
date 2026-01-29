from fastapi import APIRouter, Depends
from app.schemas.requests import TextToSummary
from app.schemas.responses import Summary
from uuid import uuid4
from app.adapters.openai_adapter import OpenAIAdapter

router = APIRouter(
    prefix = "/summary_maker",
    tags = ["summary_maker"]
)

@router.post("/get_summary_and_ctas")
async def get_summary_and_ctas(text_to_summary: TextToSummary) -> Summary:
    
    # Invoke OpenAI adapter

    # Store in memory the result
    # Output with id, summary and call to actions or next steps base on the transcript analysis
    return Summary(id=uuid4(), summary=text_to_summary.text_to_process, ctas=["cta1", "cta2"])










@router.get("/get_summary_and_ctas_by_id")
async def get_summary_and_ctas_by_id(id: int):
    # Get Summary from id from memory
    return {"summary": "summary", "ctas": ["cta1", "cta2"]}

@router.get("/async_get_summary_and_ctas")
async def async_get_summary_and_ctas(list_of_text_to_summary: list[TextToSummary]):
    # Async version of get_summary_and_ctas for multiple requests
    return {"summary": "summary", "ctas": ["cta1", "cta2"]}
