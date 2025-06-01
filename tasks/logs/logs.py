from pyinfra import host, logger
from pyinfra.operations import files, server

stack_path = "/opt/stacks/logs/"

files.directory(
    name="Create logs directory",
    path=stack_path,
    present=True,
    user="setup",
    group="setup"
)

files.put(
    name="Copy the logs compose file",
    src="tasks/logs/compose.yaml",
    dest=stack_path + "compose.yaml",
    mode="644",
    user="setup",
    group="setup"
)

files.sync(
    name="Sync dataconfig files",
    src="tasks/logs/conf",
    dest=stack_path + "conf",
    delete=True
)

server.shell(
    name="Compose up logs",
    commands=["cd " + stack_path + " && docker compose up -d"]
)
