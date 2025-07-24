from pyinfra import host, logger
from pyinfra.operations import files, server

immich_path = "/opt/stacks/immich/"

files.directory(
    name="Create immich directory",
    path="/opt/stacks/immich",
    present=True,
    user="setup",
    group="setup"
)

files.download(
    name="Download the immich compose file",
    src="https://github.com/immich-app/immich/releases/latest/download/docker-compose.yml",
    dest="/opt/stacks/immich/compose.yaml",
    user="setup",
    group="setup"
)

files.template(
    name="Generate Immich configuration file",
    src="tasks/immich/immich-config.json.j2",
    dest="/opt/stacks/immich/immich-config.json",
    public_domain=host.data.caddy_public_domain,
    mode="644",
    user="setup",
    group="setup"
)

files.template(
    name="Override some settings in docker compose",
    src="tasks/immich/compose.override.yaml.j2",
    dest="/opt/stacks/immich/compose.override.yaml",
    nfs_server=host.data.nfs_server,
    nfs_path=host.data.nfs_server_path_prefix + "immich",
    mode="644",
    user="setup",
    group="setup"
)

files.download(
    name="Download the immich .env file",
    src="https://github.com/immich-app/immich/releases/latest/download/example.env",
    dest="/opt/stacks/immich/.env",
    user="setup",
    group="setup"
)

files.line(
    name="Set immich timezone to EU-Berlin",
    path="/opt/stacks/immich/.env",
    line="# TZ=Etc/UTC",
    replace="TZ=Europe/Berlin",
    present=True
)

files.line(
    name="Set upload location to NFS based volume",
    path="/opt/stacks/immich/.env",
    line="UPLOAD_LOCATION=./library",
    replace="UPLOAD_LOCATION=immich_upload_location",
    present=True
)

files.line(
    name="Make use of immich configuration file",
    path="/opt/stacks/immich/.env",
    line="IMMICH_CONFIG_FILE=/opt/stacks/immich/immich-config.json",
    present=True
)

server.shell(
    name="Compose up immich",
    commands=["cd /opt/stacks/immich && docker compose up -d -y --force-recreate"]
)
