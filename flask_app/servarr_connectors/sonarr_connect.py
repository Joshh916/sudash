import requests
from os import environ, path
from dotenv import load_dotenv
from pprint import pprint

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, 'unitarr.conf'))

key = environ.get('SONARR_KEY')
address = environ.get('SONARR_IP')
path = environ.get('SONARR_PATH')
protocol = environ.get('SONARR_PROTOCOL')
port = environ.get('SONARR_PORT')
conn = f'{protocol}://{address}:{port}/api/v3/'

default_settings = {
    "monitored":True,
    "qualityProfileId":1,
    "rootFolderPath": path, 
    "languageProfileId": 1, 
    "addOptions":{"searchForMissingEpisodes": True}
}
headers={'accept': 'application/json', 'x-api-key':key}

def search_sonarr(search_str):
    # return requests.get(sonarr_conn + 'wanted/missing/23?apikey=' + key)
    return requests.get(conn + 'series/lookup' + '?term=' + search_str, headers=headers)

def add_show(show):
    show.update(default_settings)
    response = requests.post(conn + 'series',  headers=headers, json=show)
    print (response.text)
    return response

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
            pprint(record)
            if record.get('title') in name:
                print(name)
                remove_stalled(record.get('id'))
                return True
        