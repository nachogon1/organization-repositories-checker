import asyncio
import sys
from pathlib import Path

import requests

# This is a bit dirty. But I need it to make imports from a script.
file = Path(__file__).resolve()
parent, top = file.parent, file.parents[1]
sys.path.append(str(top))

import aioschedule as schedule

from configs import APP_URL, GITHUB_ORGANIZATION, GITHUB_TOKEN
from model.step import Step
from scheduler.tools import check_steps

response = requests.get(f"{APP_URL}/api/steps")
steps = [Step(**step) for step in response.json()]
schedule.every().day.at("09:00").do(
    check_steps,
    organization_name=GITHUB_ORGANIZATION,
    token=GITHUB_TOKEN,
    steps=steps,
)

loop = asyncio.get_event_loop()
while True:
    loop.run_until_complete(schedule.run_pending())
