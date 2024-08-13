from transmission_rpc import Client
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, 'unitarr.conf'))

protocol = environ.get('TRANSMISSION_PROTOCOL')
port = environ.get('TRANSMISSION_PORT')
host = environ.get('TRANSMISSION_HOST')
username = environ.get('TRANSMISSION_HOST')
passwd = environ.get('TRANSMISSION_HOST')
hosts = None
clients = []
if '[' in host:
    hosts = host.strip('[]').replace(" ","").split(',')
else:
    hosts = [host]

if len(hosts) > 0:
    for host in hosts:
        clients.append(Client(protocol=protocol, host=host, port=port, username=username, password=passwd, path='/transmission/rpc'))


def get_active_downloads():
    active_downloads = []
    downloads = []
    for client in clients:
        active_downloads += client.get_torrents()
    for download in active_downloads:
        downloads.append({"name":download.name, "status":download.status, "complete":download.percent_complete, "is_stalled":download.is_stalled})
    return downloads

