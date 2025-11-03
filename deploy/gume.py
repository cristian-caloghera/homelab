from pyinfra import local, config

config.SUDO = True

local.include("tasks/update-upgrade.py")
local.include("tasks/monitoring.py")
local.include("tasks/auto-upgrades.py")
local.include("tasks/data-storage.py")
local.include("tasks/docker.py")
#local.include("tasks/dockge/dockge.py")
local.include("tasks/mumble/mumble.py")
local.include("tasks/minecraft/minecraft.py")