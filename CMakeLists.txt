# Copyright (c) 2025 Rafael Carbonell Lázaro (racarla96)
# Licensed under the Creative Commons Attribution 4.0 International License (CC BY 4.0)
# See: https://creativecommons.org/licenses/by/4.0/

cmake_minimum_required(VERSION 3.16)
project(caddy_ai2_ros2_control_system_bicycle_controller LANGUAGES CXX)

# Establecer el estándar C++20 para todo el proyecto
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS ON)

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(controller_manager REQUIRED)
find_package(hardware_interface REQUIRED)
find_package(joint_state_broadcaster REQUIRED)
find_package(ros2_control REQUIRED)

# Paquetes personalizados
find_package(caddy_ai2_ros2_control_system_steering_driver REQUIRED)
find_package(caddy_ai2_ros2_control_system_traction_driver REQUIRED)
find_package(caddy_ai2_ros2_common REQUIRED)

# Este paquete no compila código C++, solo proporciona:
# - controlador (posiblemente ya compilado en otro lugar o como plugin)
# - archivos de configuración YAML
# - archivos de lanzamiento (launch)

# Instalar archivos de configuración
install(
  DIRECTORY bringup
  DESTINATION share/${PROJECT_NAME}
)

# Instalar archivos de lanzamiento
install(
  DIRECTORY bringup/
  DESTINATION share/${PROJECT_NAME}
)

# Exportación para ament
ament_package()