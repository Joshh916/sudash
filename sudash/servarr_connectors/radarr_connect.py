import requests
from os import environ
from .settings import RADARR_IP, RADARR_KEY, RADARR_PATH, RADARR_PORT, RADARR_PROTOCOL

conn = f'{RADARR_PROTOCOL}://{RADARR_IP}:{RADARR_PORT}/api/v3/'
default_settings = {
    "monitored":True,
    "qualityProfileId":1,
    "rootFolderPath": RADARR_PATH,
    "addOptions":{"searchForMovie": True}
}

headers={'accept': 'application/json', 'x-api-key':RADARR_KEY}

def search_radarr(search_str):
    return requests.get(conn + 'movie/lookup' + '?term=' + search_str, headers=headers)

def add_movie(movie):
    movie.update(default_settings)
    return requests.post(conn + 'movie',  headers=headers, json=movie)

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
        