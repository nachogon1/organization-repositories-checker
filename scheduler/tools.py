import aiohttp
import yaml
from fastapi import HTTPException
from loguru import logger

from configs import GITHUB_URL


def create_report(checkup_dict):
    """Reports the missing steps from each repository."""
    for repository in checkup_dict:
        if checkup_dict[repository]:
            logger.info(
                f"{repository} is missing {checkup_dict[repository]} steps."
            )
        else:
            logger.info(f"{repository} has no steps.")


def check_job_steps(job_steps_dict, list_required_steps):
    """Check the steps from a job and return the missing ones."""
    check_up_dict = dict([(job, []) for job in job_steps_dict])
    for job in job_steps_dict:
        for step in list_required_steps:
            if step not in job_steps_dict[job]:
                check_up_dict[job] += [step]
    return check_up_dict


def get_job_steps_dict(yml_file):
    """Get all jobs from a config.yml"""
    job_steps_dict = {}
    if "jobs" in yml_file:
        for job in yml_file["jobs"]:
            if "steps" in yml_file["jobs"][job]:
                job_steps_dict[job] = yml_file["jobs"][job]["steps"]
            else:
                job_steps_dict[job] = ["This job has no steps."]
        return job_steps_dict


class Github:
    def __init__(self, organization_name, token=None):

        self.organization_name = organization_name
        self.token = f"token {token}"
        self.headers = {"Authorization": self.token}
        self.session = aiohttp.ClientSession(headers=self.headers)
        self.checkup_dict = {}


def parse_yml(yml):
    try:
        return yaml.safe_load(yml)
    except yaml.YAMLError as exc:
        logger.error(exc)


async def check_steps(organization_name, token, steps=[]):
    github = Github(organization_name, token=token)
    async with github.session as session:
        async with session.get(
            f"{GITHUB_URL}/orgs/{github.organization_name}/repos"
        ) as resp:
            texts = await resp.json()
            if resp.status != 200:
                raise HTTPException(
                    status_code=resp.status,
                    detail=f"{resp.status} trying to log to git.",
                )  # This is a terrible error handling.
        for text in texts:
            async with session.get(
                f'{GITHUB_URL}/repos/{github.organization_name}/{text["name"]}'
                f"/contents/.circleci/config.yml"
            ) as resp:
                repo_download_url = (await resp.json())["download_url"]
            async with session.get(repo_download_url) as resp:
                config_yml = await resp.text()
                yml_parsed = parse_yml(config_yml)
                steps_parsed = [parse_yml(step.command) for step in steps]
                job_steps_dict = get_job_steps_dict(yml_parsed)
                if job_steps_dict:
                    github.checkup_dict[text["name"]] = {"jobs": {}}
                    github.checkup_dict[text["name"]]["jobs"] = check_job_steps(
                        job_steps_dict, steps_parsed
                    )
                    github.checkup_dict[text["name"]]["status"] = "compliant"
                    for job in github.checkup_dict[text["name"]]["jobs"]:
                        print(github.checkup_dict[text["name"]]["jobs"][job] == [])
                        if github.checkup_dict[text["name"]]["jobs"][job]:
                            github.checkup_dict[text["name"]]["status"] = "not-compliant"
                else:
                    github.checkup_dict[text["name"]] = "This repository has no jobs."
        # Print works better for CLI scripts.
        print("Repository missing steps", github.checkup_dict)
        return github.checkup_dict
