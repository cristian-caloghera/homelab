import private_data 
from pyinfra import config, logger, host
from pyinfra.operations import pkg, files, zfs, server, python, crontab
from pyinfra.facts.server import Sysctl

config.SUDO = False

pkg.packages(
    name="Install needed packages (base)",
    packages=[
        "nano",
        "bash",
        "smartmontools",
        "node_exporter"]
)

files.line(
    name="Enable daily fetching of updates",
    path="/etc/crontab",
    line='@daily                                  root    freebsd-update cron'
)

cpu_temp_driver = None
sysctls = host.get_fact(Sysctl)
logger.info(sysctls['hw.model']) 
# sometimes this is a list and sometimes this is a string
# for whatever reason
# so skip for now, take care later
#for text in sysctls['hw.model']:
#text = sysctls['hw.model']
#if 'AMD' in text:
#    cpu_temp_driver = 'amd'
#if 'Intel' in text:
#    cpu_temp_driver = 'core'

#files.line(
#    name="Enable reporting of CPU temps",
#    path="/boot/loader.conf",
#    line=cpu_temp_driver + 'temp_load="YES"',
#)

files.line(
    name="Enable ZFS on boot",
    path="/etc/rc.conf",
    line='zfs_enable="YES"',
)

server.shell(
    name="Start ZFS",
    commands="service zfs restart"
)

# Sync local files/tempdir to remote /tmp/tempdir
files.sync(
    name="Upload scripts",
    src="tasks/freebsd/scripts",
    dest="/root/scripts",
    delete=True,
    mode="755",
    user="root",
    group="wheel"
)

files.line(
    name="Extend crontab PATH",
    path="/var/cron/tabs/root",
    line="^PATH=.*",
    replace='PATH=/etc:/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/sbin:/usr/local/bin'
)

# simple example for a crontab
crontab.crontab(
    name="Crontab ZFS scrub",
    cron_name="ZFS scrubber",
    command='/root/scripts/scrubber.sh',
    day_of_month=1,
    hour=0,
    minute=0
)

files.line(
    name="Enable node exporter",
    path="/etc/rc.conf",
    line='node_exporter_enable="YES"',
)

server.shell(
    name="Start node exporter",
    commands="service node_exporter restart"
)

node_exporter_scripts = '/root/scripts'

# On FreeBSD the node exporter service provides the following variable:
# which is set by default, so let's just use that
# node_exporter_textfile_dir (string):  Set directory that node_exporter will watch
#               Default is "/var/tmp/node_exporter".
# see: /usr/local/etc/rc.d/node_exporter

crontab.crontab(
    name="Crontab node exporter ZFS Pool",
    cron_name="node exporter zpool",
    command=node_exporter_scripts + '/node_exporter_textfile_metric.sh ' + node_exporter_scripts + '/zfs_zpool.sh /var/tmp/node_exporter',
    hour=16,
    minute=10
)

crontab.crontab(
    name="Crontab node exporter SMARTmon",
    cron_name="node exporter smartmon",
    command=node_exporter_scripts + '/node_exporter_textfile_metric.sh ' + node_exporter_scripts + '/smartmon.sh /var/tmp/node_exporter',
    hour=16,
    minute=05
)

crontab.crontab(
    name="Crontab node exporter updates",
    cron_name="node exporter updates",
    command=node_exporter_scripts + '/node_exporter_textfile_metric.sh ' + node_exporter_scripts + '/freebsd_update_info.sh /var/tmp/node_exporter',
    hour=16,
    minute=0
)

files.line(
    name="Enable NFS",
    path="/etc/rc.conf",
    line='nfs_server_enable="YES"'
)

files.line(
    name="Also enable NFSv4",
    path="/etc/rc.conf",
    line='nfsv4_server_enable="YES"'
)


becap_host = private_data.get('becap_host')

if host.name == becap_host:
    server.user_authorized_keys(
        name="Add SSH key for secure access",
        user="root",
        group="wheel",
        public_keys=["tasks/.private/id_ed25519_homelab_key.pub"],
    )
