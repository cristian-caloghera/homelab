import private_data
from pyinfra import config

ssh_user         = private_data.get('STORAGE_SSH_USER')
ssh_password     = private_data.get('STORAGE_SSH_PASSWORD')
