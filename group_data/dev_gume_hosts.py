import private_data

from group_data.all_services_hosts import *

nfs_server                = private_data.get('dev_nfs_server')
nfs_server_path_prefix    = ":appdata/"
mumble_server_password    = private_data.get('mumble_server_password')
caddy_base_domain         = "wut?"

_sudo_password   = private_data.get('SUDO_PASSWORD')