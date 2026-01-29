import fastapi
from app.routers import summary

app = fastapi.FastAPI()

app.include_router(summary.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    fastapi.run(app, host="[IP_ADDRESS]", port=8000)