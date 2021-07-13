from fastapi import FastAPI

from api.steps import steps_router

app = FastAPI()

app.include_router(steps_router, prefix="/api/steps")