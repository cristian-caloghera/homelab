from pyinfra.operations import files, apt

from io import StringIO

apt.packages(
  name="Install unattended-upgrades",
  packages=["unattended-upgrades", "apt-listchanges"]
)

apt_conf_52_unattended_upgrades = StringIO("""Unattended-Upgrade::Origins-Pattern {
        "origin=*";
};
""")

files.template(
  name="Configure unattended-upgrades",
  src=apt_conf_52_unattended_upgrades,
  dest="/etc/apt/apt.conf.d/52unattended-upgrades-local",
  mode="644"
)

apt_conf_20_auto_upgrades = StringIO("""APT::Periodic::Update-Package-Lists "1";
APT::Periodic::Unattended-Upgrade "1";
""")

files.template(
  name="Enable unattended-upgrades",
  src=apt_conf_20_auto_upgrades,
  dest="/etc/apt/apt.conf.d/20auto-upgrades",
  mode="644"
)
