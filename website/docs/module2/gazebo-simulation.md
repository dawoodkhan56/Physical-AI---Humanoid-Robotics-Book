---
sidebar_position: 2
title: Gazebo Simulation - Physics, Gravity, and Collisions
---

# Gazebo Simulation: Physics, Gravity, and Collisions

## Introduction to Gazebo

Gazebo is a powerful open-source 3D robotics simulator that provides realistic physics simulation, high-quality rendering, and accurate sensor simulation. It's an essential tool in robotics development, allowing you to test algorithms, train AI models, and validate robot behaviors in a safe, virtual environment before deploying to physical hardware.

## Physics Simulation in Gazebo

### Physics Engines
Gazebo supports multiple physics engines:
- **ODE (Open Dynamics Engine)**: The default, suitable for most robotics applications
- **Bullet**: Good for contact-rich scenarios and robot simulation
- **Simbody**: High-performance engine for articulated systems
- **DART**: Advanced kinematics and dynamics library

### Physics Parameters
The physics simulation is controlled through the `<physics>` tag in world files:

```xml
<physics type="ode">
  <max_step_size>0.001</max_step_size>
  <real_time_factor>1</real_time_factor>
  <real_time_update_rate>1000</real_time_update_rate>
  <gravity>0 0 -9.8</gravity>
</physics>
```

Key parameters:
- `max_step_size`: Simulation time step (smaller is more accurate but slower)
- `real_time_factor`: Target simulation speed vs real time (1.0 = real time)
- `real_time_update_rate`: Update frequency in Hz
- `gravity`: Gravitational acceleration vector (x, y, z)

## Gravity Simulation

Gravity is a fundamental force in physics simulation. In Gazebo, gravity affects all bodies with mass. The default gravity vector is (0, 0, -9.8) m/s², simulating Earth's gravity.

### Custom Gravity
You can modify gravity in a world file:
```xml
<world name="custom_gravity_world">
  <gravity>0 0 -1.62</gravity>  <!-- Moon gravity -->
  <!-- ... rest of world definition ... -->
</world>
```

For planets or zero-gravity environments, you can set appropriate values:
- Earth: (0, 0, -9.8) m/s²
- Moon: (0, 0, -1.62) m/s²
- Mars: (0, 0, -3.71) m/s²
- Zero-G: (0, 0, 0) m/s²

## Collision Simulation

### Collision Detection
Gazebo provides robust collision detection between objects:
- **Surface properties**: Friction, restitution (bounciness), and contact parameters
- **Collision shapes**: Boxes, spheres, cylinders, meshes, or custom shapes
- **Contact detection**: Accurate detection of when objects touch

### Surface Parameters
Fine-tune collision behavior with surface properties:

```xml
<gazebo reference="link_name">
  <collision>
    <surface>
      <friction>
        <ode>
          <mu>1.0</mu>
          <mu2>1.0</mu2>
        </ode>
      </friction>
      <bounce>
        <restitution_coefficient>0.1</restitution_coefficient>
        <threshold>100000</threshold>
      </bounce>
      <contact>
        <ode>
          <kp>1e+16</kp>
          <kd>1e+13</kd>
          <max_vel>100.0</max_vel>
          <min_depth>0.001</min_depth>
        </ode>
      </contact>
    </surface>
  </collision>
</gazebo>
```

Parameters explained:
- `mu`, `mu2`: Friction coefficients (static and dynamic)
- `restitution_coefficient`: How bouncy collisions are (0=not bouncy, 1=very bouncy)
- `kp`, `kd`: Spring and damper coefficients for contact simulation
- `min_depth`: Minimum penetration depth before contact force is applied

## Building Complex Environments

### Creating Worlds
World files combine models, physics settings, and lighting:

```xml
<sdf version="1.6">
  <world name="my_world">
    <!-- Physics engine configuration -->
    <physics type="ode">
      <max_step_size>0.001</max_step_size>
      <real_time_factor>1</real_time_factor>
      <real_time_update_rate>1000</real_time_update_rate>
      <gravity>0 0 -9.8</gravity>
    </physics>

    <!-- Lighting -->
    <light name="sun" type="directional">
      <cast_shadows>true</cast_shadows>
      <pose>0 0 10 0 0 0</pose>
      <diffuse>0.8 0.8 0.8 1</diffuse>
      <specular>0.2 0.2 0.2 1</specular>
      <attenuation>
        <range>1000</range>
        <constant>0.9</constant>
        <linear>0.01</linear>
        <quadratic>0.001</quadratic>
      </attenuation>
      <direction>-0.2 0.5 -0.8</direction>
    </light>

    <!-- Ground plane -->
    <model name="ground_plane">
      <static>true</static>
      <link name="link">
        <collision name="collision">
          <geometry>
            <plane>
              <normal>0 0 1</normal>
              <size>100 100</size>
            </plane>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <plane>
              <normal>0 0 1</normal>
              <size>100 100</size>
            </plane>
          </geometry>
          <material>
            <ambient>0.8 0.8 0.8 1</ambient>
            <diffuse>0.8 0.8 0.8 1</diffuse>
          </material>
        </visual>
      </link>
    </model>

    <!-- Insert your robot model here -->
    <include>
      <uri>model://my_robot</uri>
    </include>
  </world>
</sdf>
```

### Physics Properties of Materials
You can customize how different materials interact by adjusting their physical properties:

```xml
<gazebo reference="floor_link">
  <collision>
    <surface>
      <friction>
        <ode>
          <mu>0.5</mu>  <!-- Medium friction -->
          <mu2>0.5</mu2>
        </ode>
      </friction>
    </surface>
  </collision>
</gazebo>

<gazebo reference="ice_link">
  <collision>
    <surface>
      <friction>
        <ode>
          <mu>0.05</mu>  <!-- Low friction -->
          <mu2>0.05</mu2>
        </ode>
      </friction>
    </surface>
  </collision>
</gazebo>
```

## Advanced Physics Features

### Buoyancy
For underwater robots, you can enable buoyancy:

```xml
<plugin name="gazebo_ros_buoyancy" filename="libgazebo_ros_buoyancy.so">
  <fluid_density>1000</fluid_density>  <!-- Water density -->
  <link_name>base_link</link_name>
</plugin>
```

### Air Resistance
For aerial vehicles, you can simulate drag:

```xml
<plugin name="gazebo_ros_drag" filename="libgazebo_ros_drag.so">
  <link_name>base_link</link_name>
  <angular_damping>0.1</angular_damping>
  <linear_damping>0.01</linear_damping>
</plugin>
```

## Optimizing Physics Simulation

### Performance Considerations
- **Step size**: Smaller steps are more accurate but slower
- **Update rate**: Higher rates are more responsive but more CPU intensive
- **Collision shapes**: Simplified shapes (boxes/spheres) are faster than complex meshes
- **Contact parameters**: Aggressive parameters (high kp/kd) can cause simulation instability

### Stability Tips
1. Start with conservative parameters and adjust as needed
2. Use appropriate time steps for your robot's dynamics
3. Ensure mass properties are realistic
4. Test with different physics engines to find the best fit
5. Monitor simulation for unrealistic behaviors (objects jittering, flying off, etc.)

## Troubleshooting Physics Issues

### Common Problems and Solutions:

1. **Objects falling through surfaces**: Increase contact parameters or check for gaps in collision surfaces
2. **Jittering**: Decrease kp/kd values or increase min_depth
3. **Objects flying apart**: Check mass properties and joint limits
4. **Stability issues**: Reduce max_step_size or adjust physics parameters

## Integration with ROS 2

Gazebo integrates seamlessly with ROS 2 through Gazebo ROS packages:

```xml
<!-- In your URDF or SDF -->
<plugin name="gazebo_ros_control" filename="libgazebo_ros_control.so">
  <robotNamespace>/my_robot</robotNamespace>
  <robotSimType>gazebo_ros_control/DefaultRobotHWSim</robotSimType>
</plugin>
```

This enables you to control your simulated robot using ROS 2 topics, just as you would a physical robot.

Understanding physics simulation in Gazebo is crucial for developing humanoid robots that can interact safely and effectively with their physical environment. Proper simulation of gravity, collisions, and physical properties allows you to test robot behaviors in a wide variety of scenarios before deployment.