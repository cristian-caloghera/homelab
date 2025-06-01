from pyinfra import host, logger
from pyinfra.operations import files, server, crontab

stack_path = "/opt/stacks/influxdb2/"

files.directory(
    name="Create InfluxDB directory",
    path=stack_path,
    present=True,
    user="setup",
    group="setup"
)

files.template(
    name="Generate Docker compose",
    src="tasks/influxdb2/compose.yaml.j2",
    dest=stack_path + "compose.yaml",
    nfs_server=host.data.nfs_server,
    nfs_path=host.data.nfs_server_path_prefix + "influxdb2",
    influxdb2_org=host.data.influxdb2_org,
    mode="644",
    user="setup",
    group="setup"
)

files.sync(
    name="Sync secrets",
    src="tasks/.private/influxdb2",
    dest=stack_path + "secrets",
    delete=True
)

server.shell(
    name="Compose up InfluxDB",
    commands=["cd " + stack_path + " && docker compose up -d -y"]
)

files.put(
    name="Copy InfluxDB2 backup script",
    src="tasks/influxdb2/backup.sh",
    dest=stack_path + "backup.sh",
)

# run every day at 01:01
crontab.crontab(
    name="Set crontab to backup InfluxDB2",
    command="/usr/bin/docker exec -i influxdb2 bash < /opt/stacks/influxdb2/backup.sh",
    hour=1,
    minute=1
)

files.put(
    name="Copy InfluxDB2 token script",
    src="tasks/influxdb2/all-access-token.sh",
    dest=stack_path + "all-access-token.sh",
)

server.shell(
    name="Get InfluxDB all access token",
    commands=["cd " + stack_path + " && echo INFLUXDB2_TOKEN=$(docker exec -i influxdb2 bash < all-access-token.sh) > .env.all-access-token"]
)
