from pyinfra import host, logger
from pyinfra.operations import files, server

grafana_path = "/opt/stacks/grafana/"

files.directory(
    name="Create Grafana directory",
    path=grafana_path,
    present=True,
    user="setup",
    group="setup"
)

files.put(
    name="Copy the Grafana compose file",
    src="tasks/grafana/compose.yaml",
    dest=grafana_path + "compose.yaml",
    mode="644",
    user="setup",
    group="setup"
)

files.sync(
    name="Sync data for provisioning",
    src="tasks/grafana/provisioning",
    dest=grafana_path + "provisioning",
    delete=True
)

server.shell(
    name="Compose up Grafana",
    commands=["cd " + grafana_path + " && docker compose up -d --force-recreate"]
)
