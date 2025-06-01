from pyinfra.operations import files, apt

apt.update(
    name="Update apt repositories",
    cache_time=3600,
)

apt.upgrade(
    name="Upgrade apt packages and remove unneeded dependencies",
    auto_remove=True
)
