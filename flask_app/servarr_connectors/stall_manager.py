from .sonarr_connect import recover_stalled as recover_stalled_sonarr
from .radarr_connect import recover_stalled as recover_stalled_radarr
from .transmission_connect import get_active_downloads
import asyncio
import schedule
import time

def check_all_stalled():
    downloads = get_active_downloads()
    for download in downloads:
        if download['is_stalled'] == True:
            recover_stalled_sonarr(download['name'])
            recover_stalled_radarr(download['name'])

async def create_stall_schedule():
    schedule.every().hour.do(check_all_stalled)
    while True:
        schedule.run_pending()
        time.sleep(59)

def start_stall_schedule():
    asyncio.run(create_stall_schedule)