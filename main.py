from fastapi import FastAPI
from app import models
from app.database import engine
from app.apis import router as api_router
import uvicorn
from dotenv import load_dotenv
import os

load_dotenv()

TEST_BUILD = os.getenv("TEST_BUILD")

app = FastAPI()

app.include_router(api_router)


def table_create_all(TEST_BUILD):
    if TEST_BUILD == 'False':
        models.Base.metadata.create_all(bind=engine)


table_create_all(TEST_BUILD)


@app.get("/")
def read_root():
    return {"message": "Carbon+Alt+Delete API is running"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
