from pyinfra import host, logger
from pyinfra.operations import files, server

stack_path = "/opt/stacks/gitea/"

files.directory(
    name="Create Gitea directory",
    path=stack_path,
    present=True,
    user="setup",
    group="setup"
)

files.template(
    name="Deploy the Gitea docker compose",
    src="tasks/gitea/compose.yaml.j2",
    dest=stack_path + "compose.yaml",
    nfs_server=host.data.nfs_server,
    nfs_path=host.data.nfs_server_path_prefix + "gitea",
    mode="644",
    user="setup",
    group="setup"
)
#files.sync(
#    name="Sync Gitea config for provisioning",
#    src="tasks/gitea/ .... ",
#    dest=stack_path + "...",
#    delete=True
#)

server.shell(
    name="Compose up Giteam",
    commands=["cd " + stack_path + " && docker compose up -d --force-recreate"]
)