#!/usr/bin/env bash
set -e
source /opt/ros/humble/setup.bash
export ROS_DOMAIN_ID=43
exec 9> /tmp/ghost_teleop.lock
flock -n 9 || { echo '幽灵键盘控制已经运行。'; exit 1; }
exec python3 "$(dirname "$0")/keyboard.py"
