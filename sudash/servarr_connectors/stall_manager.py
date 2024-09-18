from .sonarr_connect import recover_stalled as recover_stalled_sonarr
from .radarr_connect import recover_stalled as recover_stalled_radarr
from .transmission_connect import get_active_downloads
import schedule
import time

def check_all_stalled():
    downloads = get_active_downloads()
    for download in downloads:
        print(download)
        if download['is_stalled'] == True:
            recover_stalled_sonarr(download.get('name'))
            recover_stalled_radarr(download.get('name'))

def start_stall_schedule():
    schedule.every(5).minutes.do(check_all_stalled)
    while True:
        schedule.run_pending()
        time.sleep(59)