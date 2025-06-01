from pyinfra import host
from pyinfra.operations import files, server

stack_path = "/opt/stacks/pihole/"

files.directory(
    name="Create stack directory",
    path=stack_path,
    present=True,
    user="setup",
    group="setup"
)

files.put(
    name="Copy the PiHole compose file",
    src="tasks/pihole/compose.yaml",
    dest=stack_path + "compose.yaml",
    mode="644",
    user="setup",
    group="setup"
)

files.put(
    name="Copy the PiHole configuration",
    src="tasks/pihole/conf/etc/pihole/pihole.toml",
    dest=stack_path + "conf/etc/pihole/pihole.toml",
    mode="644",
    user="setup",
    group="setup",
    create_remote_dir=True
)

server.shell(
    name="Compose up PiHole",
    commands=["cd " +stack_path + " && docker compose up -d --force-recreate"],
)
