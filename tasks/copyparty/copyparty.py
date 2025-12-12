from pyinfra import host, logger
from pyinfra.operations import files, server, docker

stack_path = "/opt/stacks/copyparty/"

files.directory(
    name="Create copyparty directory",
    path=stack_path,
    present=True,
    user="setup",
    group="setup"
)

files.template(
    name="Deploy the copyparty docker compose",
    src="tasks/copyparty/compose.j2.yaml",
    dest=stack_path + "compose.yaml",
    nfs_server=host.data.nfs_server,
    nfs_path=host.data.nfs_server_path_prefix + "copyparty",
    mode="644",
    user="setup",
    group="setup"
)

files.sync(
    name="Sync config files",
    src="tasks/copyparty/cfg",
    dest=stack_path + "cfg",
    user="appdata",
    group="appdata"
)

server.shell(
    name="Compose up mumble",
    commands=["cd " + stack_path + " && docker compose up -d -y"]
)
