from pyinfra import host, logger
from pyinfra.operations import files, apt, systemd, docker
from pyinfra.facts.server import LinuxDistribution
from pyinfra.facts.deb import DebArch

import json
import os
from io import StringIO

apt.packages(
    packages=["ca-certificates", "curl"],
)

files.directory(
    name="Make sure apt keyring is present",
    path="/etc/apt/keyrings",
    present=True,
    user="root",
    group="root",
    mode="0655"
)

files.download(
    name="Download the Docker repo file",
    src="https://download.docker.com/linux/debian/gpg",
    dest="/etc/apt/keyrings/docker.asc",
    mode="a+r"
)

deb_version_codename = host.get_fact(LinuxDistribution)["release_meta"]["VERSION_CODENAME"]
deb_arch = host.get_fact(DebArch)

apt.repo(
    name="Add Docker key to apt keyring",
    src="deb [arch=" + deb_arch + " signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian " +
        deb_version_codename  + " stable",
    present=True,
    filename="docker"
)

apt.packages(
    name="Install Docker CE",
    packages=["docker-ce", "docker-ce-cli", "containerd.io", "docker-buildx-plugin", "docker-compose-plugin"],
    update=True
)

new_data_root = host.data.docker_data_root
if new_data_root:
    template = StringIO("""{
    "data-root": "{{ new_data_root }}"
}
""")

docker_config = files.template(
    name="Set custom Docker data root",
    src=template,
    dest="/etc/docker/daemon.json",
    new_data_root=new_data_root
)

systemd.service(
    name="Restart Docker service",
    service="docker",
    restarted=True,
    _if=docker_config.did_change
)

docker.network(
    name="Set up dedicated network for reverse proxying",
    network="reverse_proxy_net",
    attachable=True,
    present=True
)

docker.network(
    name="Set up dedicated network for home metrics",
    network="home_metrics",
    attachable=True,
    present=True
)
