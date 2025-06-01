from pyinfra import host, logger
from pyinfra.operations import files, server

stack_path = "/opt/stacks/mosquitto/"

files.directory(
    name="Create Mosquitto directory",
    path=stack_path,
    present=True,
    user="setup",
    group="setup"
)

files.put(
    name="Copy the Mosquitto compose file",
    src="tasks/mosquitto/compose.yaml",
    dest=stack_path + "compose.yaml",
    mode="644",
    user="setup",
    group="setup"
)

files.put(
    name="Copy the Mosquitto configuration file",
    src="tasks/mosquitto/config/mosquitto.conf",
    dest=stack_path + "config/mosquitto.conf",
    mode="644",
    user="setup",
    group="setup",
    create_remote_dir=True
)

server.shell(
    name="Compose up mosquitto",
    commands=["cd " + stack_path + " && docker compose up -d --force-recreate"]
)
