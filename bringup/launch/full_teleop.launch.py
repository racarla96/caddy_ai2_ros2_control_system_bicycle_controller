from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import Command
from launch.substitutions import FindExecutable
from launch_ros.actions import Node
from caddy_ai2_ros2_common.launch_utils import read_update_rate_from_controller_yaml

def generate_launch_description():

    # Paths a configuraciones y URDFs
    traction_pkg = "caddy_ai2_ros2_control_system_traction_driver"
    steering_pkg = "caddy_ai2_ros2_control_system_steering_driver"

    traction_config = PathJoinSubstitution([FindPackageShare(traction_pkg), "bringup", "config", "system_traction.yaml"])
    steering_config = PathJoinSubstitution([FindPackageShare(steering_pkg), "bringup", "config", "system_steering.yaml"])

    traction_urdf = Command([
        PathJoinSubstitution([FindExecutable(name="xacro")]),
        " ",
        PathJoinSubstitution([FindPackageShare(traction_pkg), "description", "urdf", "system_traction.urdf.xacro"]),
        " ",
        f"update_rate:={read_update_rate_from_controller_yaml(traction_config)}",
    ])

    steering_urdf = Command([
        PathJoinSubstitution([FindExecutable(name="xacro")]),
        " ",
        PathJoinSubstitution([FindPackageShare(steering_pkg), "description", "urdf", "system_steering.urdf.xacro"]),
        " ",
        f"update_rate:={read_update_rate_from_controller_yaml(steering_config)}",
    ])

    # Combina las descripciones URDF en un solo diccionario
    robot_description = {
        "robot_description_traction": traction_urdf,
        "robot_description_steering": steering_urdf,
    }

    traction_robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        namespace="traction",
        output="both",
        parameters=[{"robot_description": traction_urdf}],
    )

    steering_robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        namespace="steering",
        output="both",
        parameters=[{"robot_description": steering_urdf}],
    )

    # Lanzar ros2_control_node para traction y steering en namespaces separados
    traction_control_node = Node(
        package="controller_manager",
        executable="ros2_control_node",
        namespace="traction",
        parameters=[{"robot_description": traction_urdf}, traction_config],
        output="both",
    )

    steering_control_node = Node(
        package="controller_manager",
        executable="ros2_control_node",
        namespace="steering",
        parameters=[{"robot_description": steering_urdf}, steering_config],
        output="both",
    )

    # Lanzar joint_state_broadcaster para cada namespace
    traction_joint_state_broadcaster = Node(
        package="controller_manager",
        executable="spawner",
        namespace="traction",
        arguments=["joint_state_broadcaster"],
        output="screen",
    )

    steering_joint_state_broadcaster = Node(
        package="controller_manager",
        executable="spawner",
        namespace="steering",
        arguments=["joint_state_broadcaster"],
        output="screen",
    )

    # Lanzar controladores específicos
    traction_velocity_controller = Node(
        package="controller_manager",
        executable="spawner",
        namespace="traction",
        arguments=["system_traction_velocity_controller"],
        output="screen",
    )

    steering_controller = Node(
        package="controller_manager",
        executable="spawner",
        namespace="steering",
        arguments=["system_steering_controller"],
        output="screen",
    )

    # === Teleop ESP32 Bridge (joy to twist) ===
    teleop_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('caddy_ai2_ros2_teleop_radio_esp32_bridge'),
                'bringup',
                'launch',
                'joy_teleop_twist.launch.py'
            ])
        ])
    )



    return LaunchDescription([
        traction_control_node,
        steering_control_node,
        traction_joint_state_broadcaster,
        steering_joint_state_broadcaster,
        traction_velocity_controller,
        steering_controller,
        teleop_launch,
    ])