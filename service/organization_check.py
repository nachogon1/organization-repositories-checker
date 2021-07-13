from core.configs import GITHUB_TOKEN, GITHUB_ORGANIZATION
from scheduler import check_steps
from fastapi import APIRouter, Query

organization_check = APIRouter()


@organization_check.get("")
async def check_organization_steps(organization_name: str = Query(default=GITHUB_ORGANIZATION), github_token: str = Query(default=GITHUB_TOKEN)):
    print("token", github_token)
    return await check_steps(organization_name, github_token)

