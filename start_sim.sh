#!/usr/bin/env bash
set -e
source /opt/ros/humble/setup.bash
export ROS_DOMAIN_ID=43
export IGN_PARTITION=ghost_sim
cd "$(dirname "$0")"
exec 9> /tmp/ghost_sim.lock
flock -n 9 || { echo '幽灵仿真已经运行。'; exit 1; }
exec ros2 launch ./sim.launch.py "$@"
