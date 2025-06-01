from pyinfra import local, host

local.include("tasks/freebsd/base-setup.py")
if host.data.get("appdata_and_vm"):
    local.include("tasks/freebsd/storage-and-vm.py")
