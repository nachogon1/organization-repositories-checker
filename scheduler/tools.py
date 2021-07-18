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
        self.session = aiohttp.ClientSession
        self.checkup_dict = {}

    @staticmethod
    def validate_response(resp):
        if resp.status != 200:
            raise HTTPException(
                status_code=resp.status,
                detail=f"{resp.status} trying to log to git.",
            )  # This is a terrible error handling.

    async def get_repositories(self):
        async with self.session(headers=self.headers) as session:
            async with session.get(
                    f"{GITHUB_URL}/orgs/{self.organization_name}/repos"
            ) as resp:
                self.validate_response(resp)
                repo_names = await resp.json()

        return repo_names

    async def get_repo_yml_url(self, repo):
        async with self.session(headers=self.headers).get(
                f'{GITHUB_URL}/repos/{self.organization_name}/{repo["name"]}'
                f"/contents/.circleci/config.yml"
        ) as resp:
            self.validate_response(resp)
            repo_download_url = (await resp.json())["download_url"]
        return repo_download_url

    async def get_config_yml(self, url):
        async with self.session(headers=self.headers).get(url) as resp:
            self.validate_response(resp)
            config_yml = await resp.text()
        return config_yml

    def analyze_repository(self, config_yml, steps, repo_name):
        yml_parsed = parse_yml(config_yml)
        job_steps_dict = get_job_steps_dict(yml_parsed)
        if job_steps_dict:
            self.checkup_dict[repo_name["name"]] = {"jobs": {}}
            self.checkup_dict[repo_name["name"]]["jobs"] = check_job_steps(
                job_steps_dict, steps
            )
            self.checkup_dict[repo_name["name"]]["status"] = "compliant"
            for job in self.checkup_dict[repo_name["name"]]["jobs"]:
                if self.checkup_dict[repo_name["name"]]["jobs"][job]:
                    self.checkup_dict[repo_name["name"]]["status"] = "not-compliant"
        else:
            self.checkup_dict[repo_name["name"]] = "This repository has no jobs."


def parse_yml(yml):
    try:
        return yaml.safe_load(yml)
    except yaml.YAMLError as exc:
        logger.error(exc)


async def check_steps(organization_name, token, steps=[]):
    """Get all repo names from an organization. Get their download urls,
    and get the config.yml files. Parse it, look for the steps and
    collect them."""
    github = Github(organization_name, token=token)

    repo_names = await github.get_repositories()
    for repo_name in repo_names:
        repo_download_url = await github.get_repo_yml_url(repo_name)
        config_yml = await github.get_config_yml(repo_download_url)
        steps_names = [step.command for step in steps]
        github.analyze_repository(config_yml, steps_names, repo_name)

    # Print works better for CLI scripts.
    print("Repository missing steps", github.checkup_dict)
    return github.checkup_dict
