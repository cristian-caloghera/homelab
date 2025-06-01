import private_data

from group_data.all_services_hosts import *

nfs_server                = private_data.get('dev_nfs_server')
caddy_base_domain         = 'dev-' + private_data.get('caddy_base_domain')
caddy_public_domain       = ""
caddy_add_local_root_cert = True

_sudo_password   = private_data.get('SUDO_PASSWORD')
