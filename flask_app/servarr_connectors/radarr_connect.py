import requests
from os import environ, path
from dotenv import load_dotenv
from pprint import pprint

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, 'unitarr.conf'))


key = environ.get('RADARR_KEY')
address = environ.get('RADARR_IP')
path = environ.get('RADARR_PATH')
protocol = environ.get('RADARR_PROTOCOL')
port = environ.get('RADARR_PORT')
conn = f'{protocol}://{address}:{port}/api/v3/'
default_settings = {
    "monitored":True,
    "qualityProfileId":1,
    "rootFolderPath": path,
    "addOptions":{"searchForMovie": True}
}

headers={'accept': 'application/json', 'x-api-key':key}

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
    print(response.status_code)
    return response

def recover_stalled(name):
    queue_response = get_queue()
    if queue_response.status_code >= 200 and queue_response.status_code <= 299:
        for record in queue_response.json()['records']:
            if record.get('title') in name:
                remove_stalled(record.get('id'))
                return True
        