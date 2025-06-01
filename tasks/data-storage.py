from pyinfra import host, logger
from pyinfra.operations import files, apt, systemd

files.directory(
    name="Create local data path",
    path=host.data.data_path,
    present=True,
    user="setup",
    group="setup",
    mode="0644"
)
