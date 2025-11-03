from pyinfra import host, logger
from pyinfra.operations import files, server, docker

stack_path = "/opt/stacks/minecraft/"

files.directory(
    name="Create minecraft directory",
    path=stack_path,
    present=True,
    user="setup",
    group="setup"
)

files.put(
    name="Deploy minecraft compose file",
    src="tasks/minecraft/compose.yaml",
    dest=stack_path + "compose.yaml",
    mode="644",
    user="setup",
    group="setup"
)

docker.network(
    name="Set up dedicated network for minecraft",
    network="minecraft",
    attachable=True,
    present=True
)

server.shell(
    name="Compose up minecraft",
    commands=["cd " + stack_path + " && docker compose up -d"]
)
