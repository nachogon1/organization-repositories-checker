import os
import sys
from pathlib import Path
import requests

file = Path(__file__).resolve()
parent, top = file.parent, file.parents[1]
sys.path.append(str(top))
print(parent)
from model.step import Step

print(os.getcwd(), __name__)

from configs import *
from scheduler.tools import *
import aioschedule as schedule
from datetime import datetime
# TODO requests get steps and add the to scheduler

response = requests.get(f"{APP_URL}/api/steps")
steps = [Step(**step) for step in response.json()]
print(steps)
print(datetime.now())
schedule.every().day.at("10:00").do(check_steps, organization_name=GITHUB_ORGANIZATION, token=GITHUB_TOKEN, steps=steps)

loop = asyncio.get_event_loop()
while True:
    loop.run_until_complete(schedule.run_pending())