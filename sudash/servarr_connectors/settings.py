from dotenv import load_dotenv
from os import environ, path, curdir

basedir = path.abspath(curdir)
load_dotenv(path.join(basedir, 'sudash.conf'))
from ast import literal_eval

# Global Variables
SONARR_KEY = environ.get('SONARR_KEY')
SONARR_IP = environ.get('SONARR_IP')
SONARR_PATH = environ.get('SONARR_PATH')
SONARR_PROTOCOL = environ.get('SONARR_PROTOCOL')
SONARR_PORT = environ.get('SONARR_PORT')

RADARR_KEY = environ.get('RADARR_KEY')
RADARR_IP = environ.get('RADARR_IP')
RADARR_PATH = environ.get('RADARR_PATH')
RADARR_PROTOCOL = environ.get('RADARR_PROTOCOL')
RADARR_PORT = environ.get('RADARR_PORT')

TRANSMISSION_ARR = literal_eval(environ.get('TRANSMISSION_ARR'))