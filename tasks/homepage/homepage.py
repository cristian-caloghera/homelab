from pyinfra import host, logger
from pyinfra.operations import files, server

stack_path = "/opt/stacks/homepage/"

files.directory(
    name="Create homepage directory",
    path=stack_path,
    present=True,
    user="setup",
    group="setup"
)

files.sync(
    name="Deploy Homepage files",
    src="tasks/homepage",
    dest=stack_path,
    exclude= ["*.py", "*.j2"],
    delete=True,
    mode="644",
    user="setup",
    group="setup"
)

server.shell(
    name="Compose up Homepage",
    commands=["cd " + stack_path + " && docker compose up -d"]
)
