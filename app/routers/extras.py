from fastapi import APIRouter, Depends
from app.schemas.requests import TextToSummary
from app.schemas.responses import Summary
from uuid import uuid4
from app.adapters.openai import OpenAIAdapter
from app.dependencies import get_llm_service_openai, get_summary_repository
from app.ports.llm import LLm
from app.prompts import SYSTEM_PROMPT, RAW_USER_PROMPT
from app.repositories.in_memory import SummaryRepository

router = APIRouter(
    prefix = "/extras",
    tags = ["extras"]
)

@router.post("/get_summary_and_ctas")
async def get_summary_and_ctas(
    text_to_summary: TextToSummary,
    llm: LLm = Depends(get_llm_service_openai),
    repository: SummaryRepository = Depends(get_summary_repository)
    ) -> Summary:
    
    summary_result = llm.run_completion(
        SYSTEM_PROMPT, 
        RAW_USER_PROMPT.format(transcript=text_to_summary.text_to_process), 
        dto = Summary)
    summary_result.id = uuid4()

    repository.save(summary_result)

    return summary_result