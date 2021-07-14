import os
print(os.getcwd(), __name__)

from configs import *
from scheduler import *
import aioschedule as schedule

# TODO requests get steps and add the to scheduler
schedule.every().day.at("10:00").do(check_steps, organization_name=GITHUB_ORGANIZATION, token=GITHUB_TOKEN)

loop = asyncio.get_event_loop()
while True:
    loop.run_until_complete(schedule.run_pending())