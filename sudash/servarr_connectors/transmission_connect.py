from transmission_rpc import Client

from .settings import TRANSMISSION_ARR

hosts = TRANSMISSION_ARR
transmission_servers = []

def setup_transmission_servers():
    if hosts.get('single') != None:
        host = hosts.get('single')
        transmission_servers.append(Client(protocol=host.get('protocol'), host=host.get('ip'), port=host.get('port'), username=host.get('user'), password=host.get('pass'), path='/transmission/rpc'))
    else:
        if hosts.get('radarr') != None:
            host = hosts.get('radarr')
            transmission_servers.append(Client(protocol=host.get('protocol'), host=host.get('ip'), port=host.get('port'), username=host.get('user'), password=host.get('pass'), path='/transmission/rpc'))
        if hosts.get('sonarr') != None:
            host = hosts.get('sonarr')
            transmission_servers.append(Client(protocol=host.get('protocol'), host=host.get('ip'), port=host.get('port'), username=host.get('user'), password=host.get('pass'), path='/transmission/rpc'))

setup_transmission_servers()

def get_active_downloads():
    active_downloads = []
    downloads = []
    for transmission_server in transmission_servers:
        active_downloads += transmission_server.get_torrents()
    for download in active_downloads:
        downloads.append({"name":download.name, "status":download.status, "complete":download.percent_complete, "is_stalled":download.is_stalled})
    return downloads

