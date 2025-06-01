# homelab

This repo show an overview of the homelab. As almost all the infrastructure and services are being defined as code, it makes sense to publish it in a code repository.

## Purpose

The purpose of the homelab was to learn and experiment with new technologies and also make it easier to organize certain files, like documents and family photos.
Here an excert of things to expect:
 * Docker Compose (container and networks)
 * Reverse proxying of web traffic secured with TLS and mTLS with Caddy
 * Some Go applications to process non-standard data
 * Grafana, InfluxDB and Prometheus for monitoring and visualizing data
 * MQTT to easily collect some data
 * Debian Linux as Docker host
 * FreeBSD
   * using bhyve for virtualization
   * using ZFS & NFS combo for data storage

## Impressions

->> insert some screenshots

## Building blocks

## Hardware

A short description of the hardware being used

### Production

Hardware is mostly an assortment of various things obtained at a low cost from internet market places, or was simply lying around the house unused.
As electricy is not cheap, care has to be taken to also get somewhat efficient hardware. The power measurement is under typical load for my use-cases.

The reason for a separate DNS/DHCP machine is because it is a critical component of the network. This avoids downtime and unnecessary question from the familiy. :)

| What for: | DNS / DHPC | Services       |
|-----------|------------|----------------|
| CPU       | AMD G415GA | AMD Ryzen 3100 |
| RAM       | 4 GB       | 128 GB ECC     |
| Storage   | 128 GiB    | 3.84 TiB       |
| Network   | 1 Gbit     | 1 Gbit         |
| Power     | 7 W        | 35 W           |

### Development

For the development environment the above machines are replaced by VMs running on a laptop.

## Deployment

The deployment is automatic and handled by [pyinfra](https://docs.pyinfra.com/en/3.x/index.html). While Ansible surely could've done the job as being more feature complete, pyinfra simply offers a supperior experience for people with a heavy coding background, because it is based on Python.

### Get started

You will need pyinfra. On Debian you can use `pipx` to automatically create virtual environments and manage them, but regular `pip` or barebones Python 3 also works.

On Debian and derivatives:
```
apt install pipx
pipx install pyinfra
pipx ensurepath
pipx inject pyinfra python-dotenv
```
Now you need to logout and login again to get the new updated `PATH` variable in your terminal, giving direct access to `pyinfra`.
At this point you can use pyinfra:
```
pyinfra <inventory> <deployment>
```

## Structure

### Inventory & Data

There are separate inventories for production and for development. Also there are two corresponding groups storing the respective data for these inventories. The differences between these sets of inventory and data are kept to a minimum. The group `all` contains data that is valid for all inventories.

### Deployments

There are two deployments possible right now: one for services and one for dns/dhcp. This repo will focus on the services, as the dns/dhcp configuration is mostly redacted for privacy.

The deployments files will references tasks under the `tasks/` directory (not necessarily all) and will execture in order. Here is an overview of the order of what is happening, steps 1-3 are generally valid for all deployments, while what comes after is pretty much deployment specific. Let's have a look at the services deployment because it is the more complex one:

1. system is updated
2. automatic updates (security) are enabled
3. the Docker engine is installed
4. Docker networks are created (e.g.: reverse proxy network)
5. Service are being installa via `docker compose`

While some services depend on others, most of these dependencies are handled by the order of operations, i.e. `dependes_on` is under utlized. Even so, because the whole deployment is execute in a single go there are no problems.

### Storage

Generally storage is handled by Docker volumes. Two kinds can observed:

 * ephemeral: hosted on the Docker host directly, it is quite small and mostly contains configuration files
 * persistent: hosted on a high reliability NFS server, and mounted as Docker NFS based volumes
 
## Private data

There is no private data stored here on purpose. All the relevant passwords, addresses, locations, etc. has been redacted out due to privacy reasons.
