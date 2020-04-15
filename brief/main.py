import logging
import os

from fastapi import FastAPI

from brief.briefs.modules import modules

app = FastAPI()

# to start uvicorn main:app --reload

logging.basicConfig()
logger = logging.getLogger(__name__)


@app.get("/")
async def read_root():
    results = {}
    for module in modules:
        try:
            results[module.name] = await module.run_brief()
        except Exception:
            logger.error(f'{module.name} had an exception.')
    return results
