from pyinfra import host, logger
from pyinfra.operations import docker

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
