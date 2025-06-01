from pyinfra import host, logger
from pyinfra.operations import files, server

stack_path = "/opt/stacks/wg-easy/"

files.directory(
    name="Create wg-easy directory",
    path=stack_path,
    present=True,
    user="setup",
    group="setup"
)

files.put(
    name="Deploy wg-easy compose file",
    src="tasks/wg-easy/compose.yaml",
    dest=stack_path + "compose.yaml",
    mode="644",
    user="setup",
    group="setup"
)

server.shell(
    name="Compose up wg-easy",
    commands=["cd " + stack_path + " && docker compose up -d"]
)
