from pyinfra import host, logger
from pyinfra.operations import files, server

stack_path = "/opt/stacks/ha-mqtt-relay/"

files.directory(
    name="Create stack directory",
    path=stack_path,
    present=True,
    user="setup",
    group="setup"
)

files.sync(
    name="Deploy ha-mqtt-relay files",
    src="tasks/ha-mqtt-relay",
    dest=stack_path,
    exclude="*.py",
    delete=True,
    mode="644",
    user="setup",
    group="setup"
)

server.shell(
    name="Compose up heizung mqtt relay",
    commands=["cd " + stack_path + " && docker compose up -d --build"]
)
