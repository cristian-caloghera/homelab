from pyinfra import local

local.include("tasks/update-upgrade.py")
local.include("tasks/monitoring.py")
local.include("tasks/auto-upgrades.py")
local.include("tasks/data-storage.py")
local.include("tasks/docker.py")
local.include("tasks/dockge/dockge.py")
local.include("tasks/pihole/pihole.py")
local.include("tasks/wg-easy/wg-easy.py")