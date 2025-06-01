from pyinfra import host
from pyinfra.operations import files, server

files.directory(
    name="Create Dockge directory",
    path="/opt/dockge",
    present=True,
    user="setup",
    group="setup"
)

files.template(
    name="Generate the private environemt variables",
    src="tasks/.private/.env.private.docker.j2",
    dest="/opt/stacks/.env.private.docker",
    base_domain=host.data.caddy_base_domain,
    create_remote_dir=True,
    mode="600",
    user="setup",
    group="setup"
)

files.download(
    name="Download the Dockge compose file",
    src="https://raw.githubusercontent.com/louislam/dockge/master/compose.yaml",
    dest="/opt/dockge/compose.yaml",
    user="setup",
    group="setup"
)

files.put(
    name="Copy the Dockge compose override file",
    src="tasks/dockge/compose.override.yaml",
    dest="/opt/dockge/compose.override.yaml",
    mode="644",
    user="setup",
    group="setup"
)

server.shell(
    name="Compose up Dockge",
    commands=["cd /opt/dockge && docker compose up -d"],
)
