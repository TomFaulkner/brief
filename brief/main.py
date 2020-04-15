import os

from fastapi import FastAPI

app = FastAPI()

# to start uvicorn main:app --reload
TASK_DIR = os.environ.get('BRIEF_DIR', 'briefs')


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
