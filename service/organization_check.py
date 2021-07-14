from configs import GITHUB_TOKEN, GITHUB_ORGANIZATION
from db.steps import StepCRUD
from scheduler.tools import check_steps
from fastapi import APIRouter, Query, Depends

organization_check = APIRouter()


@organization_check.get("/organization-check")
async def check_organization_steps(organization_name: str = Query(default=GITHUB_ORGANIZATION, alias="organization-name"), github_token: str = Query(default=GITHUB_TOKEN, alias="github-token"), step_crud: StepCRUD = Depends()):
    steps = step_crud.get_all()
    return await check_steps(organization_name, github_token, steps)

