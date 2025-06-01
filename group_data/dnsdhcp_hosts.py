import private_data
from pyinfra import config

config.SUDO = True

ssh_user         = private_data.get('SSH_USER')
ssh_password     = private_data.get('SSH_PASSWORD')
_sudo_password   = private_data.get('SUDO_PASSWORD')

caddy_base_domain = private_data.get('caddy_base_domain')

data_path        = "/mnt/data"
docker_data_root = "/mnt/data/docker-data-root"
