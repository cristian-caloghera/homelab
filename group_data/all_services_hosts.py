import private_data
from pyinfra import config

config.SUDO = True

ssh_user         = private_data.get('SSH_USER')
ssh_password     = private_data.get('SSH_PASSWORD')

data_path        = "/mnt/data"
docker_data_root = "/mnt/data/docker-data-root"

ftp_scanner_user = private_data.get('ftp_scanner_user')
ftp_scanner_password = private_data.get('ftp_scanner_password')

nfs_server_path_prefix    = ":appdata/"
influxdb2_org             = private_data.get('influxdb2_org')
