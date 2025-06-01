from pyinfra import host, logger
from pyinfra.operations import files, server

stack_path = "/opt/stacks/heatoil-reader/"

files.directory(
    name="Create stack directory",
    path=stack_path,
    present=True,
    user="setup",
    group="setup"
)

files.sync(
    name="Deploy heatoil-reader files",
    src="tasks/heatoil-reader",
    dest=stack_path,
    exclude="*.py",
    delete=True,
    mode="644",
    user="setup",
    group="setup"
)

server.shell(
    name="Compose up heatoil-reader",
    commands=["cd " + stack_path + " && docker compose up -d --build"]
)
