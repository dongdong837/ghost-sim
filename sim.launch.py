"""Ghost simulation, bridges, model display, camera and flight control."""
from pathlib import Path
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
ROOT = Path(__file__).parent


def static_tf(name,parent,child,xyz,rpy=(0,0,0)):
    x,y,z = xyz
    roll,pitch,yaw = rpy
    return Node(package='tf2_ros',executable='static_transform_publisher',name=name,
                arguments=['--x',str(x),'--y',str(y),'--z',str(z),'--roll',str(roll),
                           '--pitch',str(pitch),'--yaw',str(yaw),'--frame-id',parent,'--child-frame-id',child])


def generate_launch_description():
    def gazebo(context):
        command = ['ign','gazebo','-r','-v','3']
        if LaunchConfiguration('gui').perform(context) != 'true':
            command.append('-s')
        return [ExecuteProcess(cmd=command+[str(ROOT/'ghost_room.sdf')],output='screen')]

    actions = [DeclareLaunchArgument('gui',default_value='false'),OpaqueFunction(function=gazebo),
               Node(package='robot_state_publisher',executable='robot_state_publisher',
                    parameters=[{'robot_description':(ROOT/'ghost_display.urdf').read_text(),'use_sim_time':True}])]
    for script in ['ground_truth_tf.py','reference_scene.py','cloud_frame.py','flight_control.py','voxel_map_node.py','navigation3d.py']:
        actions.append(ExecuteProcess(cmd=['python3',str(ROOT/script),'--ros-args','-p','use_sim_time:=true'],output='screen'))
    actions.append(Node(package='ros_gz_bridge',executable='parameter_bridge',name='ghost_bridge',
                        arguments=[
                            '/model/ghost/cmd_vel@geometry_msgs/msg/Twist]ignition.msgs.Twist',
                            '/model/ghost/pose@tf2_msgs/msg/TFMessage[ignition.msgs.Pose_V',
                            '/clock@rosgraph_msgs/msg/Clock[ignition.msgs.Clock',
                            '/camera/image@sensor_msgs/msg/Image[ignition.msgs.Image',
                            '/camera/depth_image@sensor_msgs/msg/Image[ignition.msgs.Image',
                            '/camera/camera_info@sensor_msgs/msg/CameraInfo[ignition.msgs.CameraInfo',
                            '/camera/points@sensor_msgs/msg/PointCloud2[ignition.msgs.PointCloudPacked'],
                        remappings=[('/model/ghost/pose','/simulation/ground_truth/poses'),
                                    ('/camera/points','/camera/points_raw')],output='screen'))
    actions.extend([static_tf('camera_mount','base_link','camera_link',(.29,0,0)),
                    static_tf('camera_optical','camera_link','camera_optical_frame',(0,0,0),
                              (-1.57079632679,0,-1.57079632679))])
    return LaunchDescription(actions)
