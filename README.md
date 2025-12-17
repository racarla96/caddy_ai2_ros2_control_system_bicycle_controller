# Caddy AI2 ROS2 Control System Bicycle Controller

## 📌 Descripción

Este paquete proporciona un sistema de control unificado para robots móviles tipo ackermann basados en la **cinemática tipo bicicleta**, integrando **tres controladores** bajo un único `controller_manager`:

- **`system_traction_velocity_controller`**: control de velocidad de las ruedas motrices.  
- **`system_steering_controller`**: control de dirección (giro del eje delantero).  
- **`bicycle_steering_controller`**: control coordinado de dirección y tracción con modelo cinemático de bicicleta.  

Además, incluye el **`joint_state_broadcaster`** para publicar estados de las articulaciones (`/joint_states`).

El sistema está configurado para operar a **500 Hz**, y está optimizado para su uso en entornos de **tiempo real** (con soporte para aislamiento de CPU y prioridad RT).

Este paquete **actúa como paquete de integración principal**, reutilizando controladores y otros componentes previamente definidos en:
- `caddy_ai2_ros2_control_system_steering_driver`
- `caddy_ai2_ros2_control_system_traction_driver`
- `caddy_ai2_ros2_common`

---

## 📦 Dependencias

### Requisitos del sistema
- **ROS 2 Jazzy** (Jellyfish)
- `ros2_control` y `ros2_controllers`
- Paquetes personalizados:
  - `caddy_ai2_ros2_control_system_steering_driver`
  - `caddy_ai2_ros2_control_system_traction_driver`
  - `caddy_ai2_ros2_common`

---

## 🛠️ Instalación

1. **Clona el paquete** en tu workspace de ROS 2:

```bash
cd ~/ros2_ws/src
git clone <URL_DEL_REPOSITORIO>  # ajusta según tu fuente
```

2. **Construye el workspace**:

```bash
cd ~/ros2_ws
colcon build --packages-select caddy_ai2_ros2_control_system_bicycle_controller
source install/setup.bash
```

> Asegúrate de que todos los paquetes dependientes ya estén construidos.

---

## ▶️ Uso

Lanza el sistema de control integrado con:

```bash
ros2 launch caddy_ai2_ros2_control_system_bicycle_controller integration.launch.py
```

Esto iniciará:
- El nodo `ros2_control_node` con `update_rate: 500 Hz`
- El `joint_state_broadcaster`
- Los tres controladores, todos en estado **activo**

### Publicaciones clave
- `/joint_states` — estados de articulaciones
- Comandos y estados de los controladores (ej. `/bicycle_steering_controller/reference`)

---

## ⚙️ Configuración

El archivo de configuración principal se encuentra en:

```
config/controllers.yaml
```

Parámetros editables:
- `update_rate`: frecuencia de control (por defecto: 500 Hz)
- Nombres de articulaciones (`joints`, `front_steering_joints`, `wheel_joints`, etc.)
- Parámetros del modelo de bicicleta: `wheelbase`, `track`

> ⚠️ **Importante**: Asegúrate de que los nombres de las articulaciones coincidan con tu modelo URDF.

---

## ⚡ Optimización en tiempo real (opcional)

Para aplicaciones críticas en tiempo real:

### 1. Aislar CPU (kernel)
Edita `/etc/default/grub`:
```bash
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash isolcpus=3 nohz_full=3 rcu_nocbs=3"
```
Ejecuta:
```bash
sudo update-grub && sudo reboot
```

### 2. Permisos de tiempo real
```bash
sudo groupadd realtime
sudo usermod -a -G realtime $USER
echo '* - rtprio 99' | sudo tee -a /etc/security/limits.conf
echo '* - memlock unlimited' | sudo tee -a /etc/security/limits.conf
```

### 3. (Opcional) Usar kernel PREEMPT_RT
Recomendado para jitter < 50 µs.

El lanzador ya incluye soporte para `taskset` y `chrt` (descomenta en `integration_launch.py` si lo usas).

---

# 👥 Autores

- **Desarrollador Principal**: Rafael Carbonell Lázaro (racarla96)
- **Proyecto**: Caddy AI2 - Proyecto CERVAREC

## 📄 Licencia

Copyright (c) 2025, Rafael Carbonell Lázaro (racarla96)

Este proyecto se distribuye bajo la licencia **Creative Commons Attribution 4.0 International (CC BY 4.0)**.

### En resumen:

✅ **Puedes:**
- Usar, modificar y redistribuir la librería
- Utilizarla en proyectos comerciales o privados
- Crear trabajos derivados

⚠️ **Debes:**
- Mantener atribución al autor/proyecto (en documentación, créditos, "About" de la aplicación, etc.)
- Indicar si se realizaron cambios
- Proporcionar un enlace a la licencia

❌ **No puedes:**
- Imponer restricciones adicionales que impidan a otros ejercer los permisos que otorga la licencia

### Texto legal completo:
https://creativecommons.org/licenses/by/4.0/legalcode

### Atribución sugerida:


Este proyecto utiliza "caddy_ai2_ros2_control_system_steering_driver"
desarrollado por Rafael Carbonell Lázaro (racarla96)
Licencia: CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/)