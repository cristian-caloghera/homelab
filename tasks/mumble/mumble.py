from pyinfra import host, logger
from pyinfra.operations import files, server, docker

stack_path = "/opt/stacks/mumble/"

files.directory(
    name="Create Mumble directory",
    path=stack_path,
    present=True,
    user="setup",
    group="setup"
)

files.directory(
    name="Create Mumble data directory",
    path=stack_path + "mumble-data",
    present=True,
    user="setup",
    group="setup"
)

# these files are pre-generated via acme.sh
# and the owenership set manually, in order for mumble to read them
# acme.sh will not change it if the file is already created                                 
files.sync(
    name="Deploy acme.sh structure for mumble.burunet.dedyn.io",
    src="tasks/.private/acmeout-mumble.burunet.dedyn.io",
    dest=stack_path + "acmeout",
    delete=True,
    mode="600",
    user="10001",
    group="10001"
)

files.directory(
    name="Create acme.sh out directory",
    path=stack_path + "acmeout",
    present=True,
    user="setup",
    group="setup"
)

files.template(
    name="Deploy Mumble docker compose",
    src="tasks/mumble/compose.yaml.j2",
    dest=stack_path + "compose.yaml",
    nfs_server=host.data.nfs_server,
    nfs_path=host.data.nfs_server_path_prefix + "mumble",
    mumble_server_password=host.data.mumble_server_password,
    mode="644",
    user="setup",
    group="setup"
)

server.shell(
    name="Compose up mumble",
    commands=["cd " + stack_path + " && docker compose up -d -y"]
)

# todo: store certificates and then on unarchive make sure key is readable by setup
# check if server is restarted on docker hook