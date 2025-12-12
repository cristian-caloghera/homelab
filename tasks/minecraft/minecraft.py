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

files.template(
    name="Deploy Minecraft Fabric docker compose",
    src="tasks/minecraft/compose.yaml.j2",
    dest=stack_path + "compose.yaml",
    nfs_server=host.data.nfs_server,
    nfs_path=host.data.nfs_server_path_prefix + "minecraft",
    mode="644",
    user="setup",
    group="setup"
)

files.put(
    name="Upload Docker compose base config",
    src="tasks/minecraft/compose.base.yaml",
    dest=stack_path + "compose.base.yaml",
    mode="644",
    user="setup",
    group="setup"
)

files.put(
    name="Upload whitelist of players",
    src="tasks/.private/minecraft/whitelist.json",
    dest=stack_path + "whitelist.json",
    mode="644",
    user="setup",
    group="setup"
)

files.put(
    name="Upload ops list of players",
    src="tasks/.private/minecraft/ops.json",
    dest=stack_path + "ops.json",
    mode="644",
    user="setup",
    group="setup"
)

server.shell(
    name="Compose up minecraft",
    commands=["cd " + stack_path + " && docker compose up -d --force-recreate --remove-orphans"]
)