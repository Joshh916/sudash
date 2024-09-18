import requests
from .settings import SONARR_IP, SONARR_KEY, SONARR_PATH, SONARR_PORT, SONARR_PROTOCOL

conn = f'{SONARR_PROTOCOL}://{SONARR_IP}:{SONARR_PORT}/api/v3/'

default_settings = {
    "monitored":True,
    "qualityProfileId":1,
    "rootFolderPath": SONARR_PATH, 
    "languageProfileId": 1, 
    "addOptions":{"searchForMissingEpisodes": True}
}
headers={'accept': 'application/json', 'x-api-key':SONARR_KEY}

def search_sonarr(search_str):
    return requests.get(conn + 'series/lookup' + '?term=' + search_str, headers=headers)

def add_show(show):
    show.update(default_settings)
    response = requests.post(conn + 'series',  headers=headers, json=show)
    return response

def get_queue():
    response = requests.get(conn + 'queue' , headers=headers)
    return response

def remove_stalled(id):
    params = '?removeFromClient=true&blocklist=true'
    response = requests.delete(conn + 'queue/' + str(id) + params, headers=headers)
    return response

def recover_stalled(name):
    queue_response = get_queue()
    if queue_response.status_code >= 200 and queue_response.status_code <= 299:
        for record in queue_response.json()['records']:
            if record.get('title') in name:
                remove_stalled(record.get('id'))
                return True
        