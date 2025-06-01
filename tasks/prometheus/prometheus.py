from pyinfra import host, logger
from pyinfra.operations import files, server

import os

stack_name = "prometheus"

stack_path = "/opt/stacks/" + stack_name + "/"

files.directory(
    name="Create " + stack_name + " directory",
    path=stack_path,
    present=True,
    user="setup",
    group="setup"
)

files.sync(
    name="Deploy " + stack_name + " files",
    src="tasks/prometheus",
    dest=stack_path,
    exclude= ["*.py", "*.j2", "*private-nodes.list*"],
    delete=True,
    mode="644",
    user="setup",
    group="setup"
)

node_targets = []
def add_node_target(hostname):
    target = '"' + hostname + ':9100"'
    node_targets.append(target)

add_node_target(host.name)
add_node_target(host.data.nfs_server)

try:
    with open('tasks/.private/prometheus/nodes.list', 'r') as file:
        for line in file:
            add_node_target(line.strip())
except Exception:
    pass

files.template(
    name="Generate node targets",
    src="tasks/prometheus/config/targets.json.j2",
    dest="/opt/stacks/prometheus/config/targets.json",
    node_targets=", ".join(node_targets),
    mode="644",
    user="setup",
    group="setup"
)

server.shell(
    name="Compose up " + stack_name,
    commands=["cd " + stack_path + " && docker compose up -d --force-recreate"]
)
