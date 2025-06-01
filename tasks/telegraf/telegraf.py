from pyinfra import host, logger
from pyinfra.operations import files, server

stack_path = "/opt/stacks/telegraf/"

files.directory(
    name="Create Telegraf directory",
    path=stack_path,
    present=True,
    user="setup",
    group="setup"
)

files.put(
    name="Copy the Telegraf compose file",
    src="tasks/telegraf/compose.yaml",
    dest=stack_path + "compose.yaml",
    mode="644",
    user="setup",
    group="setup"
)

files.put(
    name="Copy the Telegraf configuration file",
    src="tasks/telegraf/config/telegraf.conf",
    dest=stack_path + "config/telegraf.conf",
    mode="644",
    user="setup",
    group="setup",
    create_remote_dir=True
)

server.shell(
    name="Compose up Telegraf",
    commands=["cd " + stack_path + " && docker compose up -d --force-recreate"]
)
