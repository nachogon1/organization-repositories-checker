import json
import yaml

import aiohttp
import asyncio

from starlette.requests import Request
from starlette.responses import Response

# from loguru import logger TODO add




def create_report(checkup_dict):
    """Reports the missing steps from each repository."""
    for repository in checkup_dict:
        if checkup_dict[repository]:
            print(f"{repository} is missing {checkup_dict[repository]} steps.")
        else:
            print(f"{repository} has no steps.")


def check_job_steps(job_steps_dict, list_required_steps):
    """Check the steps from a job and return the missing ones."""
    print(list_required_steps)
    if job_steps_dict:
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
            print(job_steps_dict, job)
            job_steps_dict[job] = yml_file["jobs"][job]["steps"]
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
        print(exc)


# TODO substitute env variables
async def check_steps(organization_name, token, steps=[]):
    github = Github(
        organization_name, token=token
    )
    #print(certifi.where())
    #print(ssl.create_default_context(cafile=certifi.where()))
    async with github.session as session:
        async with session.get(
            f"https://api.github.com/orgs/{github.organization_name}/repos"
        ) as resp:
            print(resp.status)
            texts = await resp.text()
            if resp.status != 200:
                raise Exception(f"{resp.status} trying to log to git.")  # TODO improve
        for text in json.loads(texts):
            print(text["name"])
            async with session.get(
                f'https://api.github.com/repos/{github.organization_name}/{text["name"]}/contents/.circleci/config.yml'
            ) as resp:
                print(resp.status)
                repo_download_url = json.loads(await resp.text())["download_url"]
            async with session.get(repo_download_url) as resp:
                print(resp.status)
                config_yml = await resp.text()
                print(yaml.safe_load(config_yml))
                yml_parsed = parse_yml(config_yml)
                steps_parsed = [parse_yml(step.command) for step in steps]
                job_steps_dict = get_job_steps_dict(yml_parsed)
                if job_steps_dict:
                    print(check_job_steps(job_steps_dict, steps))  # TODO add steps
                    github.checkup_dict[text["name"]] = check_job_steps(
                        job_steps_dict, steps_parsed
                    )
                else:
                    github.checkup_dict[text["name"]] = "Has no steps."
        print("Repository missing steps", github.checkup_dict)
        return github.checkup_dict

