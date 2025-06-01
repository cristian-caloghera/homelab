from pyinfra import local

local.include("tasks/update-upgrade.py")
local.include("tasks/monitoring.py")
local.include("tasks/auto-upgrades.py")
