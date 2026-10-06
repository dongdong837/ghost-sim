#!/usr/bin/env bash
set -e
source /opt/ros/humble/setup.bash
export ROS_DOMAIN_ID=43
exec python3 "$(dirname "$0")/ghost_ai.py" "$@"
