from pyinfra.operations import server

server.packages(
    name="Install Prometheus node exporter",
    packages=["prometheus-node-exporter"]
)

# prom files seem to generated by default here:
#/var/lib/prometheus/node-exporter/nvme.prom
#/var/lib/prometheus/node-exporter/apt.prom
