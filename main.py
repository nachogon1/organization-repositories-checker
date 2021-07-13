from fastapi import FastAPI

from api.steps import steps_router
from service.organization_check import organization_check

app = FastAPI()

app.include_router(steps_router, prefix="/api/steps")
app.include_router(organization_check, prefix="/service/steps")