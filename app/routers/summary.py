from fastapi import APIRouter, Depends, Query
from app.schemas.requests import TextToSummary
from app.schemas.responses import SummaryResponse
from app.schemas.llm_responses import SummaryLLMOutput
from uuid import uuid4
from app.dependencies import get_llm_service_openai, get_summary_repository
from app.ports.llm import LLm
from app.ports.summary_repository import SummaryRepository
from app.domain.entities import Summary
from app.prompts import SYSTEM_PROMPT, RAW_USER_PROMPT
import asyncio
from typing import Annotated

example = """In today’s volatile market, the traditional "command and control" style of leadership isn't just outdated—it’s a liability. Many leaders find themselves trapped in the 'Expert Paradox,' where they feel they must have all the answers to maintain authority. However, this often creates a bottleneck, stifling team creativity and leading to burnout for the person at the top.
True leadership coaching focuses on the transition from being a manager who directs to a coach who multiplies. By adopting a "curiosity-first" framework, leaders can empower their teams to solve complex problems independently. This involves mastering the art of the powerful question, active listening, and providing radical candor that fosters growth rather than defensiveness. When a leader shifts from solving every problem to building the problem-solving capacity of their people, the entire organization gains the agility needed to thrive in uncertain times."""

router = APIRouter(
    prefix = "/summary_maker",
    tags = ["summary_maker"]
)

@router.get("/get_summary_and_ctas")
async def get_summary_and_ctas(
    text_to_summary: TextToSummary = example,
    llm: LLm = Depends(get_llm_service_openai),
    repository: SummaryRepository = Depends(get_summary_repository)
    ) -> SummaryResponse:
    
    llm_result = llm.run_completion(
        SYSTEM_PROMPT, 
        RAW_USER_PROMPT.format(transcript=text_to_summary), 
        dto = SummaryLLMOutput)

    summary_entity = Summary(
        id = str(uuid4()),
        content=llm_result.content,
        ctas=llm_result.ctas
        )

    repository.save(summary_entity)

    return SummaryResponse.from_entity(summary_entity)

@router.get("/get_summary_and_ctas_by_id")
async def get_summary_and_ctas_by_id(
    id: str, 
    repository: SummaryRepository = Depends(get_summary_repository)) -> Summary:

    summary = repository.get_by_id(id)

    if summary is None:
        raise HTTPException(status_code=404, detail="Summary not found")
    else:
        return summary

@router.post("/async_get_summary_and_ctas")
async def async_single_get_summary_and_ctas(
    list_of_texts_to_summarize: list[TextToSummary] = [example,example],
    llm: LLm = Depends(get_llm_service_openai),
    repository: SummaryRepository = Depends(get_summary_repository)) -> list[SummaryResponse]:

    async def process_one_request(text_to_summarize: TextToSummary) -> Summary:
        llm_result = await llm.run_completion_async(
        SYSTEM_PROMPT, 
        RAW_USER_PROMPT.format(transcript=text_to_summarize), 
        dto = SummaryLLMOutput)

        summary_entity = Summary(
            id = str(uuid4()),
            content=llm_result.content,
            ctas=llm_result.ctas
            )

        repository.save(summary_entity)

        return summary_entity

    tasks = [process_one_request(item) for item in list_of_texts_to_summarize]

    summary_entities = await asyncio.gather(*tasks)
    return [SummaryResponse.from_entity(s) for s in summary_entities]
