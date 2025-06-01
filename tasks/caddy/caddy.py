from pyinfra import host, logger
from pyinfra.operations import files, server

caddy_path = "/opt/stacks/caddy/"

files.directory(
    name="Create Caddy directory",
    path=caddy_path,
    present=True,
    user="setup",
    group="setup"
)

files.put(
    name="Copy the Caddy compose file",
    src="tasks/caddy/compose.yaml",
    dest=caddy_path + "compose.yaml",
    mode="644",
    user="setup",
    group="setup"
)

files.template(
    name="Create Caddyfile from template",
    src="tasks/caddy/Caddyfile.j2",
    dest=caddy_path + "conf/Caddyfile",
    base_domain=host.data.caddy_base_domain,
    public_domain=host.data.caddy_public_domain,
    local_root_cert=host.data.caddy_add_local_root_cert,
    create_remote_dir=True,
    mode="644",
    user="setup",
    group="setup"
  )

files.put(
    name="Copy the Caddy mTLS certificate",
    src="tasks/.private/caddy/certs/client.crt",
    dest=caddy_path + "conf/client.crt",
    mode="644",
    user="setup",
    group="setup"
)

server.shell(
    name="Compose up caddy",
    commands=["cd /opt/stacks/caddy && docker compose up -d"]
)

if host.data.caddy_add_local_root_cert:

    root_ca_path="/usr/local/share/ca-certificates/caddy-root-ca.crt"

    server.shell(
        name="Extract Caddy root certificate authority",
        commands=["cd /opt/stacks/caddy && \
                    docker compose cp \
                    caddy:/data/caddy/pki/authorities/local/root.crt " + root_ca_path]
    )

    files.file(
        name="Make Caddy certificate file read-only",
        path=root_ca_path,
        mode="644"
    )

    server.shell(
        name="Add Caddy CA to system CAs",
        commands=["update-ca-certificates"]
    )

    files.put(
        name="Add Caddy root CA to Firefox",
        src="tasks/caddy/firefox-policies.json",
        dest="/etc/firefox/policies/policies.json",
        create_remote_dir=True,
        mode="644"
    )

    server.shell(
        name="Reload Caddy configuration",
        commands=["cd /opt/stacks/caddy && docker compose exec -w /etc/caddy caddy caddy reload"]
    )
