from fastapi import APIRouter, Depends
from app.schemas.requests import TextToSummary
from app.schemas.responses import Summary
from uuid import uuid4
from app.adapters.openai import OpenAIAdapter
from app.dependencies import get_llm_service_openai, get_summary_repository
from app.ports.llm import LLm
from app.prompts import SYSTEM_PROMPT, RAW_USER_PROMPT
from app.repositories.in_memory import SummaryRepository
import asyncio

router = APIRouter(
    prefix = "/summary_maker",
    tags = ["summary_maker"]
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


@router.get("/get_summary_and_ctas_by_id")
async def get_summary_and_ctas_by_id(
    id: str, 
    repository: SummaryRepository = Depends(get_summary_repository)) -> Summary:

    summary = repository.get_by_id(id)

    if summary is None:
        raise HTTPException(status_code=404, detail="Summary not found")
    else:
        return summary

@router.get("/async_get_summary_and_ctas")
async def async_single_get_summary_and_ctas(
    list_of_text_to_summary: list[TextToSummary],
    llm: LLm = Depends(get_llm_service_openai),
    repository: SummaryRepository = Depends(get_summary_repository)) -> list[Summary]:

    async def process_one_request(text_to_summary: TextToSummary) -> Summary:
        summary_result = await llm.run_completion_async(
        SYSTEM_PROMPT, 
        RAW_USER_PROMPT.format(transcript=text_to_summary.text_to_process), 
        dto = Summary)
        summary_result.id = uuid4()

        repository.save(summary_result)

        return summary_result

    tasks = [process_one_request(item) for item in list_of_text_to_summary]

    results = await asyncio.gather(*tasks)
    return list[results]
