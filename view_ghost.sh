#!/usr/bin/env bash
set -e
source /opt/ros/humble/setup.bash
export ROS_DOMAIN_ID=43
exec rviz2 -d "$(dirname "$0")/ghost.rviz" --ros-args -p use_sim_time:=true
