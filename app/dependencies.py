from app.ports.llm import LLm
from app.configurations import settings
from app.adapters.openai import OpenAIAdapter
from app.repositories.in_memory import InMemorySummaryRepository


def get_llm_service_openai() -> LLm:
    return OpenAIAdapter(model=settings.OPENAI_MODEL, api_key=settings.OPENAI_API_KEY)


_summary_repository: InMemorySummaryRepository | None = None

def get_summary_repository() -> InMemorySummaryRepository:
    if _summary_repository is None:
        raise RuntimeError("Summary repository not initialized")
    return _summary_repository

def set_summary_repository(repository: InMemorySummaryRepository) -> None:
    global _summary_repository
    _summary_repository = repository
