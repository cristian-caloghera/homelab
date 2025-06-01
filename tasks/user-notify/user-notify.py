from pyinfra import host, logger
from pyinfra.operations import files, server

stack_path = "/opt/stacks/user-notify/"

files.directory(
    name="Create stack directory",
    path=stack_path,
    present=True,
    user="setup",
    group="setup"
)

files.sync(
    name="Deploy user-notify files",
    src="tasks/user-notify",
    dest=stack_path,
    exclude="*.py",
    delete=True,
    mode="644",
    user="setup",
    group="setup"
)

files.put(
    name="Upload the keys to access the users",
    src="tasks/.private/id_ed25519_homelab_key",
    dest=stack_path + "id_ed25519",
    mode="600",
)

files.put(
    name="Upload the script for user notfication",
    src="tasks/.private/notify-d.sh",
    dest=stack_path + "notify-d.sh",
    mode="500",
)


server.shell(
    name="Compose up user notify",
    commands=["cd " + stack_path + " && docker compose up -d --build"]
)
