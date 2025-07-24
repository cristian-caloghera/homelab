from pyinfra import host, logger
from pyinfra.operations import files, server

stack_path = "/opt/stacks/immich-public-proxy/"

files.directory(
    name="Create Immich Public Proxy directory",
    path=stack_path,
    present=True,
    user="setup",
    group="setup"
)

files.put(
    name="Deploy Immich Public Proxy compose file",
    src="tasks/immich-public-proxy/compose.yaml",
    dest=stack_path + "compose.yaml",
    mode="644",
    user="setup",
    group="setup"
)

server.shell(
    name="Compose up Immich Public Proxy",
    commands=["cd " + stack_path + " && docker compose up -d"]
)
