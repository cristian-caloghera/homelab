from pyinfra import config, logger, host
from pyinfra.operations import pkg, files, zfs, server, python, crontab
from pyinfra.facts.server import Users

from io import StringIO

config.SUDO = False

pkg.packages(
    name="Install needed packages",
    packages=[
        "vm-bhyve",
        "grub2-bhyve",
        "bhyve-firmware"]
)

# assume the pool has been already created
# because each machine has a different kinf of pool setup

# pool name might differ from host to host
zfs_pool="data"

datasets = [
    zfs_pool + "/appdata/immich",
    zfs_pool + "/appdata/influxdb2/data",
    zfs_pool + "/appdata/influxdb2/config",
    zfs_pool + "/appdata/influxdb2/backup",
    zfs_pool + "/appdata/paperless-exports",
    zfs_pool + "/vm"
]

for dataset in datasets:
    zfs.dataset(dataset, recursive=True)


files.line(
    name="Enable VM (bhyve)",
    path="/etc/rc.conf",
    line='vm_enable="YES"',
)

files.line(
    name="Set VM storage",
    path="/etc/rc.conf",
    line='vm_dir="zfs:' + zfs_pool + '/vm"',
)

users = host.get_fact(Users, )

if not "appdata" in users:
    # create appdata user
    # use the FreeBSD bulk method, that also supports setting the password in a plain way
    user_list=StringIO("""# name:uid:gid:class:change:expire:gecos:home_dir:shell:password
appdata:10001::::::/nonexistent::appdata
""")
    files.put(
        name="Upload list of users",
        src=user_list,
        dest="/root/user.list",
    )
    server.shell(
        name="Create additional users in bulk",
        commands="adduser -f /root/user.list"
    )

files.directory(
    name="Set appdata permissions on /mnt/data/appdata",
    path="/mnt/data/appdata",
    user="appdata",
    group="appdata",
    recursive=True
)

etc_exports = StringIO("""V4: /mnt/data

# NFSv4
/mnt/data/appdata/immich -maproot=appdata:appdata
/mnt/data/appdata/influxdb2/data -maproot=appdata:appdata
/mnt/data/appdata/influxdb2/config -maproot=appdata:appdata
/mnt/data/appdata/influxdb2/backup -maproot=appdata:appdata
/mnt/data/appdata/paperless-exports -maproot=appdata:appdata
""")

files.put(
    name="Update NFS exports",
    src=etc_exports,
    dest="/etc/exports",
    user="root",
    group="wheel",
    mode="0644"
)

server.shell(
    name="Reload NFS configuration",
    commands="service mountd onereload"
)

# there should a scan of the back-up host here
# but becap is online only on demand and
# to avoid the hassle in a private homelab
# just skip the host key checking
# ssh.key_scan ... <-- skip this part

files.directory(
    name="Ensure /root/.ssh is there",
    path="/root/.ssh",
    user="root",
    group="wheel",
    mode="700"
)

files.put(
    name="Upload the keys to access the backup",
    src="tasks/.private/id_ed25519_homelab_key",
    dest="/root/.ssh/id_ed25519",
    mode="600",
)

files.put(
    name="Upload the legacy keys to access the power",
    src="tasks/.private/id_rsa_homelab_legacy_key",
    dest="/root/.ssh/id_rsa_homelab_legacy_key",
    mode="600",
)

files.directory(
    name="Ensure log directory for back run is there",
    path="/var/log/becap-run",
    user="root",
    group="wheel",
)

crontab.crontab(
    name="Crontab becap run",
    cron_name="becap run",
    command='/root/scripts/becap-run.sh > /var/log/becap-run/last.log',
    day_of_month=21,
    hour=17,
    minute=40
)
