# caddy_ai2_ros2_control_system_bicycle_controller/launch/integration_launch.py
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, RegisterEventHandler
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.event_handlers import OnProcessStart

def generate_launch_description():
    config_file = PathJoinSubstitution([
        FindPackageShare("caddy_ai2_ros2_control_system_bicycle_controller"),
        "config",
        "controllers.yaml"
    ])

    # controller_manager node
    control_node = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[config_file],
        output="both",
        # OPCIONAL: para tiempo real (véase sección 4)
        # prefix=["taskset -c 3 chrt -f 90 "],
    )

    # Spawners
    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster", "--controller-manager", "/controller_manager"],
    )

    traction_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["system_traction_velocity_controller", "--controller-manager", "/controller_manager"],
    )

    steering_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["system_steering_controller", "--controller-manager", "/controller_manager"],
    )

    bicycle_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["bicycle_steering_controller", "--controller-manager", "/controller_manager"],
    )

    # Secuencia de activación
    return LaunchDescription([
        control_node,

        RegisterEventHandler(
            OnProcessStart(
                target_action=control_node,
                on_start=[joint_state_broadcaster_spawner],
            )
        ),
        RegisterEventHandler(
            OnProcessStart(
                target_action=joint_state_broadcaster_spawner,
                on_start=[traction_spawner, steering_spawner, bicycle_spawner],
            )
        ),
    ])