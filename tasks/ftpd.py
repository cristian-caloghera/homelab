from pyinfra import host, logger
from pyinfra.operations import files, server

server.packages(
    name="Install vsftpd as FTP server",
    packages=["vsftpd"]
)

files.line(
    name="Allow users to write to via FTP",
    path="/etc/vsftpd.conf",
    line="#write_enable=YES",
    replace="write_enable=YES",
    present=True
)

files.line(
    name="chroot users that connect via FTP",
    path="/etc/vsftpd.conf",
    line=".chroot_local_user=.*",
    replace="chroot_local_user=YES",
    present=True
)

server.service(
    name="Reload vsftpd to apply new configuration",
    service="vsftpd",
    reloaded=True,
)
