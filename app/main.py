import fastapi
from fastapi import FastAPI
from app.routers import summary, extras
from contextlib import asynccontextmanager
from app.dependencies import set_summary_repository
from app.repositories.in_memory import InMemorySummaryRepository

@asynccontextmanager
async def lifespan(app: FastAPI):
    repository = InMemorySummaryRepository()
    set_summary_repository(repository)

    yield

app = fastapi.FastAPI(lifespan = lifespan)

app.include_router(summary.router)
app.include_router(extras.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    fastapi.run(app, host="[IP_ADDRESS]", port=8000)