import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.substitutions import PathJoinSubstitution, Command, FindExecutable, LaunchConfiguration
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

import xacro

def generate_launch_description():
    ld = LaunchDescription()
    use_sim_time = LaunchConfiguration('use_sim_time')
    #path of package + config + ros2_controllers.yaml
    ros2_controllers_path = "src/joints_control_pkg/config/ros2_controller.yaml"

    xacro_file = os.path.join("src/joints_control_pkg",'description','so101_new_calib.urdf.xacro')
    robot_description_config = xacro.process_file(xacro_file)
    params = {'robot_description': robot_description_config.toxml(), 'use_sim_time': use_sim_time}
    #Pre-existing ros2 node
    #Subscribes to /joint_states and publishes 3d transforms to /tf and /tf_static topics
    robot_state_publisher_node = Node(
        package = "robot_state_publisher",
        executable="robot_state_publisher",
        output="both",
        parameters=[params]
    )
    ros2_control_node = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[ros2_controllers_path],
        remappings=[
            ("/controller_manager/robot_description", "/robot_description"),
        ],
        output="screen",
    )

    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["pid_controller", "--controller-manager", "/controller_manager"],
    )

    pid_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster", "--controller-manager", "/controller_manager"],
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use sim time if true'),
        ros2_control_node,
        robot_state_publisher_node,
        joint_state_broadcaster_spawner,
        pid_controller_spawner
        #velocity_converter,
        
    ])
    
