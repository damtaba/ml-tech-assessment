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
    prefix = "/extras",
    tags = ["extras"]
)

@router.get("/get_summaries_ids")
async def get_summaries_ids(repository: SummaryRepository = Depends(get_summary_repository))-> list[str]:
    return repository.list_ids()