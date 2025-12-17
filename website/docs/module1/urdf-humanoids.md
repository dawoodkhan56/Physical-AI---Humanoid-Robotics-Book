---
sidebar_position: 4
title: Understanding URDF for Humanoids
---

# Understanding URDF (Unified Robot Description Format) for Humanoids

## What is URDF?

URDF (Unified Robot Description Format) is an XML-based format used in ROS to describe robot models. It defines the physical and visual properties of a robot, including its kinematic structure, visual appearance, and physical properties. For humanoid robots, URDF is particularly important because of their complex kinematic structures with multiple degrees of freedom.

## URDF Components for Humanoid Robots

A humanoid robot URDF typically includes:

- **Links**: Rigid bodies that represent physical parts of the robot (head, torso, arms, legs)
- **Joints**: Connections between links that define how they move relative to each other
- **Visual**: Describes how the robot appears (meshes, colors, materials)
- **Collision**: Defines collision geometry for physics simulation
- **Inertial**: Physical properties like mass and moments of inertia

## Basic URDF Structure

```xml
<?xml version="1.0"?>
<robot name="my_humanoid_robot">
  <!-- Define links -->
  <link name="base_link">
    <!-- Link properties -->
  </link>

  <!-- Define joints -->
  <joint name="joint_name" type="revolute">
    <parent link="parent_link"/>
    <child link="child_link"/>
    <!-- Joint properties -->
  </joint>
</robot>
```

## Detailed URDF Example for a Simple Humanoid

```xml
<?xml version="1.0"?>
<robot name="simple_humanoid">
  <!-- Base and Torso -->
  <link name="base_link">
    <visual>
      <geometry>
        <box size="0.2 0.1 0.3"/>
      </geometry>
      <material name="blue">
        <color rgba="0 0 1 0.8"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <box size="0.2 0.1 0.3"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="10"/>
      <origin xyz="0 0 0"/>
      <inertia ixx="0.1" ixy="0" ixz="0" iyy="0.1" iyz="0" izz="0.1"/>
    </inertial>
  </link>

  <!-- Head -->
  <link name="head">
    <visual>
      <geometry>
        <sphere radius="0.1"/>
      </geometry>
      <material name="white">
        <color rgba="1 1 1 0.8"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <sphere radius="0.1"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1"/>
      <origin xyz="0 0 0"/>
      <inertia ixx="0.001" ixy="0" ixz="0" iyy="0.001" iyz="0" izz="0.001"/>
    </inertial>
  </link>

  <joint name="torso_head_joint" type="revolute">
    <parent link="base_link"/>
    <child link="head"/>
    <origin xyz="0 0 0.25"/>
    <axis xyz="0 1 0"/>
    <limit lower="-1.57" upper="1.57" effort="100" velocity="1"/>
  </joint>

  <!-- Left Arm -->
  <link name="left_upper_arm">
    <visual>
      <geometry>
        <cylinder length="0.3" radius="0.05"/>
      </geometry>
      <material name="red">
        <color rgba="1 0 0 0.8"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <cylinder length="0.3" radius="0.05"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.5"/>
      <origin xyz="0 0 -0.15"/>
      <inertia ixx="0.01" ixy="0" ixz="0" iyy="0.01" iyz="0" izz="0.001"/>
    </inertial>
  </link>

  <joint name="left_shoulder_joint" type="revolute">
    <parent link="base_link"/>
    <child link="left_upper_arm"/>
    <origin xyz="0.15 0 0.1"/>
    <axis xyz="0 1 0"/>
    <limit lower="-1.57" upper="1.57" effort="100" velocity="1"/>
  </joint>

  <!-- Right Arm -->
  <link name="right_upper_arm">
    <visual>
      <geometry>
        <cylinder length="0.3" radius="0.05"/>
      </geometry>
      <material name="red">
        <color rgba="1 0 0 0.8"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <cylinder length="0.3" radius="0.05"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.5"/>
      <origin xyz="0 0 -0.15"/>
      <inertia ixx="0.01" ixy="0" ixz="0" iyy="0.01" iyz="0" izz="0.001"/>
    </inertial>
  </link>

  <joint name="right_shoulder_joint" type="revolute">
    <parent link="base_link"/>
    <child link="right_upper_arm"/>
    <origin xyz="-0.15 0 0.1"/>
    <axis xyz="0 1 0"/>
    <limit lower="-1.57" upper="1.57" effort="100" velocity="1"/>
  </joint>

  <!-- Left Leg -->
  <link name="left_upper_leg">
    <visual>
      <geometry>
        <cylinder length="0.4" radius="0.06"/>
      </geometry>
      <material name="gray">
        <color rgba="0.5 0.5 0.5 0.8"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <cylinder length="0.4" radius="0.06"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="2"/>
      <origin xyz="0 0 -0.2"/>
      <inertia ixx="0.02" ixy="0" ixz="0" iyy="0.02" iyz="0" izz="0.002"/>
    </inertial>
  </link>

  <joint name="left_hip_joint" type="revolute">
    <parent link="base_link"/>
    <child link="left_upper_leg"/>
    <origin xyz="0.07 0 -0.15"/>
    <axis xyz="0 1 0"/>
    <limit lower="-1.57" upper="1.57" effort="100" velocity="1"/>
  </joint>

  <!-- Right Leg -->
  <link name="right_upper_leg">
    <visual>
      <geometry>
        <cylinder length="0.4" radius="0.06"/>
      </geometry>
      <material name="gray">
        <color rgba="0.5 0.5 0.5 0.8"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <cylinder length="0.4" radius="0.06"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="2"/>
      <origin xyz="0 0 -0.2"/>
      <inertia ixx="0.02" ixy="0" ixz="0" iyy="0.02" iyz="0" izz="0.002"/>
    </inertial>
  </link>

  <joint name="right_hip_joint" type="revolute">
    <parent link="base_link"/>
    <child link="right_upper_leg"/>
    <origin xyz="-0.07 0 -0.15"/>
    <axis xyz="0 1 0"/>
    <limit lower="-1.57" upper="1.57" effort="100" velocity="1"/>
  </joint>
</robot>
```

## Joint Types for Humanoid Robots

Humanoid robots require various joint types to achieve human-like movement:

- **Revolute**: Rotational joints with a defined range of motion (e.g., elbows, knees)
- **Continuous**: Rotational joints without limits (e.g., wrists, neck)
- **Prismatic**: Linear sliding joints (rarely used in humanoid robots)
- **Fixed**: Rigid connections (e.g., attaching sensors)

## URDF for Complex Humanoid Kinematics

For more realistic humanoid robots, consider these additional elements:

### Transmission Elements
```xml
<transmission name="left_elbow_trans">
  <type>transmission_interface/SimpleTransmission</type>
  <joint name="left_elbow_joint">
    <hardwareInterface>PositionJointInterface</hardwareInterface>
  </joint>
  <actuator name="left_elbow_motor">
    <mechanicalReduction>1</mechanicalReduction>
  </actuator>
</transmission>
```

### Safety Controllers
```xml
<gazebo reference="left_shoulder_joint">
  <implicitSpringDamper>1</implicitSpringDamper>
</gazebo>
```

### Gazebo-Specific Properties
```xml
<gazebo reference="head">
  <material>Gazebo/Blue</material>
  <mu1>0.2</mu1>
  <mu2>0.2</mu2>
</gazebo>
```

## Advanced URDF Concepts for Humanoids

### 1. Robot with Sensors
Humanoid robots often include sensors:

```xml
<link name="camera_link">
  <visual>
    <geometry>
      <box size="0.02 0.04 0.02"/>
    </geometry>
  </visual>
  <collision>
    <geometry>
      <box size="0.02 0.04 0.02"/>
    </geometry>
  </collision>
  <inertial>
    <mass value="0.1"/>
    <inertia ixx="0.001" ixy="0" ixz="0" iyy="0.001" iyz="0" izz="0.001"/>
  </inertial>
</link>

<joint name="camera_joint" type="fixed">
  <parent link="head"/>
  <child link="camera_link"/>
  <origin xyz="0.05 0 0.05" rpy="0 0 0"/>
</joint>

<gazebo reference="camera_link">
  <sensor type="camera" name="camera1">
    <update_rate>30.0</update_rate>
    <camera name="head_camera">
      <horizontal_fov>1.3962634</horizontal_fov>
      <image>
        <width>800</width>
        <height>800</height>
        <format>R8G8B8</format>
      </image>
      <clip>
        <near>0.02</near>
        <far>300</far>
      </clip>
    </camera>
    <plugin name="camera_controller" filename="libgazebo_ros_camera.so">
      <alwaysOn>true</alwaysOn>
      <updateRate>0.0</updateRate>
      <cameraName>camera1</cameraName>
      <imageTopicName>image_raw</imageTopicName>
      <cameraInfoTopicName>camera_info</cameraInfoTopicName>
      <frameName>camera_link</frameName>
    </plugin>
  </sensor>
</gazebo>
```

### 2. Mimic Joints
For symmetric movements:

```xml
<joint name="right_elbow_joint" type="revolute">
  <parent link="right_upper_arm"/>
  <child link="right_lower_arm"/>
  <origin xyz="0 0 -0.3"/>
  <axis xyz="0 1 0"/>
  <limit lower="0" upper="2.5" effort="100" velocity="1"/>
  <mimic joint="left_elbow_joint" multiplier="1" offset="0"/>
</joint>
```

## Best Practices for Humanoid URDF

1. **Accurate Kinematics**: Ensure the kinematic chain properly represents the physical robot
2. **Realistic Mass Properties**: Use accurate mass, center of mass, and inertia values
3. **Proper Joint Limits**: Define realistic joint limits to prevent damage or instability
4. **Collision Geometry**: Use simplified but accurate collision meshes
5. **Visual Meshes**: Use detailed meshes for visualization but simpler ones for collision detection
6. **Consistent Naming**: Use clear, consistent naming conventions
7. **Documentation**: Comment your URDF for easier maintenance

## URDF Validation and Tools

### Checking URDF Validity
```bash
# Check syntax
check_urdf /path/to/robot.urdf

# Display information about the robot
urdf_to_graphiz /path/to/robot.urdf
```

### Visualizing URDF
- Use RViz to visualize the robot in ROS
- Use Gazebo for physics simulation
- Use tools like `joint_state_publisher_gui` to move joints interactively

## Integrating URDF with ROS 2

Once your URDF is complete, integrate it with ROS 2:

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from tf2_ros import TransformBroadcaster
from geometry_msgs.msg import TransformStamped

class StatePublisher(Node):
    def __init__(self):
        super().__init__('state_publisher')
        self.joint_pub = self.create_publisher(JointState, 'joint_states', 10)
        self.broadcaster = TransformBroadcaster(self, 10)
        self.timer = self.create_timer(0.1, self.publish_states)
        self.t = 0.0

    def publish_states(self):
        msg = JointState()
        msg.name = ['left_shoulder_joint', 'right_shoulder_joint']
        msg.position = [0.1 * sin(self.t), 0.1 * cos(self.t)]
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'base_link'
        self.joint_pub.publish(msg)
        self.t += 0.1

def main(args=None):
    rclpy.init(args=args)
    node = StatePublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
```

URDF is fundamental to humanoid robotics, enabling proper simulation, visualization, and control of complex multi-joint robots. With a well-structured URDF, your humanoid robot can be simulated in Gazebo, visualized in RViz, and controlled using ROS 2.