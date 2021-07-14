from configs import GITHUB_TOKEN, GITHUB_ORGANIZATION
from db.steps import StepCRUD
from scheduler.tools import check_steps
from fastapi import APIRouter, Query, Depends

organization_check = APIRouter()


@organization_check.get("")
async def check_organization_steps(organization_name: str = Query(default=GITHUB_ORGANIZATION), github_token: str = Query(default=GITHUB_TOKEN), step_crud: StepCRUD = Depends()):
    print("token", github_token)
    steps = step_crud.get_all()
    print("STEEEPS", steps)
    return await check_steps(organization_name, github_token, steps)

