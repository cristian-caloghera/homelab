# Homelab

A Homelab setup with the following highlights:
 - per room climate monitoring
 - outside climate
 - heating, electricity (and water soon) consumption
 - image and documents hosting and backups
 - home lab infrastructure and services logs

## Some impressions

Because in this case some pictures (click for larger version) really do tell more than words:

<table>
  <tr>
    <td><img src="doc/heating-overview.png" alt="Heating Overview"></td>
    <td><img src="doc/home-overview.png" alt="Home Overview"></td>
  </tr>
  <tr>
    <td><img src="doc/infra-overview.png" alt="Infra Overview"></td>
    <td><img src="doc/room-details.png" alt="Room Details"></td>
  </tr>
  <tr>
    <td colspan="2"><img src="doc/service-logs.png" alt="Service Logs" style="width:100%;"></td>
  </tr>
</table>

## High level architecture

Depiction of the high level building blocks making up the homelab setup. To keep it
concise some details have been ommitted.

 * deployment is done with [pyinfra](https://pyinfra.com/)
 * setup is based on [Go](https://docs.docker.com/compose/)
 * custom programmings in [Go](https://go.dev/) (and some Shell)

<img src="doc/high-level-blocks.png" alt="high level architecture">
