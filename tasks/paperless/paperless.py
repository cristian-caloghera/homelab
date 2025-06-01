from pyinfra import host, logger
from pyinfra.operations import files, server, crontab
import subprocess
import sys

stack_path = "/opt/stacks/paperless/"

files.directory(
    name="Create Paperless NGX stack directory",
    path=stack_path,
    present=True,
    user="setup",
    group="setup"
)

# assuming some FTP server is already installed
# crypt might be removed in future Pythons
# $y$ is yescrypt in use by Debian
# shell alternative is: echo "user:password" | chpasswd

# WARNING: in addition to the aboce Paperless NGX insists
# to change ownership of mounted directories
# i.e. it will change the ownership of this directory to whatever
# is defined in docker-compose.env file
# so, now id 1001:1001 happen to be ftpscanner

fu = host.data.ftp_scanner_user
fp = host.data.ftp_scanner_password

server.user(
    name="Create the FTP scanner user",
    user=fu,
    ensure_home=True
)

server.shell(
    name="Set FTP user's password in a reliable way",
    commands=['echo "' + fu + ':' + fp + '" | chpasswd'],
)

files.directory(
    name="Make FTP user home read-only to secure chroot",
    path="/home/" + fu,
    user="root",
    group="root",
    mode="555"  # r-xr-xr-x
)

files.directory(
    name="Make FTP user's upload directory",
    path="/home/" + fu + "/upload",
    user=fu,
    group=fu,
    mode="755" # rwxr-xr-x
)

# do the NFS backup mount via script because PyInfra way is not really there yet
# it fails if the mount directory does not exists, however if created and
# mounted successfully once it will fail because the permission on the
# have changed because of the mount and will try to create the directory again

server.packages(
    name="Install nfs-common",
    packages=["nfs-common"]
)

nfs_server = host.data.nfs_server
nfs_export = "appdata/paperless-exports"
mount_point = "/mnt/data/appdata/paperless-exports"

server.script(
    name="Ensure NFS mount for Paperless backups",
    src="tasks/paperless/backup-mount.sh",
    args=(nfs_server, nfs_export, mount_point)
)

files.sync(
    name="Deploy Paperless files",
    src="tasks/paperless",
    dest=stack_path,
    exclude= ["*.py", "*.j2"],
    delete=True,
    mode="644",
    user="setup",
    group="setup"
)

server.shell(
    name="Compose up Paperless NGX",
    commands=["cd " + stack_path + " && docker compose up -d --force-recreate"]
)

# run a backup every day at 01:30
crontab.crontab(
    name="Set crontab to backup Paperless",
    command="/usr/bin/bash /opt/stacks/paperless/backup.sh",
    hour=1,
    minute=30
)
