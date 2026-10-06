#!/usr/bin/env bash
set -e
source /opt/ros/humble/setup.bash
export ROS_DOMAIN_ID=43
exec timeout 10 ros2 service call /ghost/cancel_navigation std_srvs/srv/Trigger '{}'
