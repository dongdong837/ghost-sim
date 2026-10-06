# Ghost Sim：大模型控制的三维幽灵机器人

A ROS 2 and Gazebo simulation of a spherical flying robot with 3D voxel mapping, autonomous XYZ navigation, RGB-D vision, and LLM-powered natural language control.

ROS 2 Humble / Gazebo Fortress 房间仿真：球形幽灵可沿 XYZ 自由飞行，支持体素地图、三维 A* 导航、RGB-D 相机和阶跃星辰自然语言目标控制。

## 环境

已验证环境：Ubuntu 22.04、ROS 2 Humble、Gazebo Fortress。先按 ROS 官方安装说明配置 Humble 软件源和 ROS 环境，再安装依赖：

```bash
sudo apt update
sudo apt install ros-humble-ros-gz ros-humble-rviz2 ros-humble-robot-state-publisher ros-humble-cv-bridge python3-numpy python3-opencv python3-yaml
```

需要图形桌面/OpenGL 上下文来渲染相机，即使 Gazebo 使用无 GUI 模式。虚拟机软件渲染可以运行，但帧率取决于机器性能。

## 快速启动

在仓库目录下，分别开三个终端运行：

```bash
./start_sim.sh
./view_ghost.sh
./teleop.sh
```

脚本自动使用 ROS_DOMAIN_ID=43 和 Gazebo 分区 ghost_sim。W/S 控制世界 ±X，A/D 控制世界 ±Y，R/F 升降，J/L 转向，空格/K 取消导航并悬停，Q 退出遥控。

## 三维导航

仿真定位就绪后，在仓库目录执行：

```bash
./navigate.sh 0 0 2.2
./navigate.sh 2.8 1.0 0.5 --yaw 1.5708
./cancel_navigation.sh
```

位置参数是 X、Y、Z（米），yaw 单独以弧度指定。RViz 粉色线是三维路线；绿色切片表示对应高度的可飞行体素。地图从已知场景碰撞几何生成，不是 SLAM。位置容差 0.06 米，朝向容差 0.10 弧度；动态障碍重规划尚未实现。

## 大模型控制

程序本地运行，模型通过阶跃星辰云端 API 调用。密钥仅通过环境变量传入：

```bash
read -rsp 'StepFun API key: ' STEPFUN_API_KEY; echo
export STEPFUN_API_KEY
./ghost_ai.sh '飞到房间中心，高度2米'
./ghost_ai.sh '降低半米'
./ghost_ai.sh '飞到绿色箱子正上方'
./ghost_ai.sh '停下'
```

`--dry-run` 调用模型并校验目标，但不移动；`--vision` 上传一帧相机图像，仅做观察问答。停止不依赖模型或密钥。API 地址/模型配置见 `ghost_ai_config.json`；可用 STEPFUN_BASE_URL、STEPFUN_LLM_MODEL、STEPFUN_VISION_MODEL 覆盖。

地标坐标来自已知场景，相对升降根据执行前实时位姿解析。模型只输出受限目标意图，本地规划器验证目标与连续路径后才执行。

## 地图与测试

启动时自动生成 0.1 米分辨率的 80×60×30 体素地图。`flight_space.npz`、运行日志与测试记录属于生成产物，不随仓库上传。

```bash
python3 -m unittest discover -s . -p 'test_*.py' -v
python3 voxel_map.py --query -1.8 1.2 1.5
```

物理仿真验收会实际移动幽灵，需在初始位置且停止遥控后单独执行：

```bash
source /opt/ros/humble/setup.bash
ROS_DOMAIN_ID=43 python3 check_flight.py
python3 check_navigation3d.py
```

模型更改后先运行 `python3 create_scene.py`，再重启仿真。当前所有障碍为轴对齐静态箱体；世界零重力，模拟理想悬浮运动，不模拟旋翼/实机飞控。若飞行控制进程被强制杀死，应停止仿真，Gazebo 速度插件不具备独立看门狗。

## 学习资料

- [代码逐句讲解](代码逐句讲解.md)：模型、传感器、TF、地图、导航、大模型及逐行源码。
- [使用与开发记录](使用与开发记录.md)：各阶段命令与本机实测结果。

文档中的 `/home/ubuntu/ghost_sim` 是开发机器原路径，其他机器请替换成实际克隆目录；所有运行脚本按自身目录定位文件。
