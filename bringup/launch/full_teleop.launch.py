from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time', default='false')

    # === Steering System ===
    steering_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('caddy_ai2_ros2_control_system_steering_driver'),
                'bringup',
                'launch',
                'system_steering.launch.py'
            ])
        ])
    )

    # === Traction System ===
    traction_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('caddy_ai2_ros2_control_system_traction_driver'),
                'bringup',
                'launch',
                'system_traction.launch.py'
            ])
        ])
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

    # Ruta al archivo YAML de configuración
    controller_params_file = PathJoinSubstitution([
        FindPackageShare('caddy_ai2_ros2_control_system_bicycle_controller'),
        'bringup',
        'config',
        'full_teleop.yaml'
    ])

    # === Opcional: Spawner del controlador bicycle_steering_controller ===
    # Solo si NO está activado automáticamente en otro launch
    bicycle_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "bicycle_steering_controller",
            "--controller-manager", "/controller_manager",
            "--param-file", controller_params_file
        ],
        output="screen"
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation time if true'
        ),
        steering_launch,
        traction_launch,
        teleop_launch,
        bicycle_controller_spawner  # Comenta esta línea si el controlador ya está activado
    ])