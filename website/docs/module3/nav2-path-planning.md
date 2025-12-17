---
sidebar_position: 4
title: Nav2 Path Planning for Bipedal Humanoid Movement
---

# Nav2 Path Planning for Bipedal Humanoid Movement

## Introduction to Navigation for Humanoid Robots

Navigation for humanoid robots presents unique challenges compared to traditional wheeled or tracked robots. Humanoid robots must navigate with bipedal locomotion, which introduces considerations for balance, step planning, gait patterns, and dynamic stability. The Navigation2 (Nav2) framework, when properly configured, can effectively handle these challenges by incorporating humanoid-specific constraints and capabilities.

## Understanding Bipedal Locomotion Challenges

### Balance and Stability
Unlike wheeled robots, humanoid robots must maintain balance while walking. This introduces several navigation constraints:
- **Center of Mass Management**: The robot must maintain its center of mass within its support polygon
- **Dynamic Balance**: Balance is maintained through continuous motion rather than static stability
- **Foot Placement**: Each step requires careful planning of foot positions

### Gait Planning Considerations
- **Step Length and Width**: Must be optimized for stability and efficiency
- **Walking Speed**: Affects stability and obstacle avoidance capabilities
- **Turning**: Requires special gait patterns for efficient direction changes
- **Terrain Adaptation**: Ability to handle stairs, slopes, and uneven surfaces

## Nav2 Architecture Overview

Nav2 consists of several key components that work together:

```
[Goals] → [Action Server] → [Planner Server] → [Controller Server] → [Robot]
                           ↓
                       [Recovery Server]
```

For humanoid robots, each component needs to be adapted to handle bipedal-specific requirements.

## Configuring Nav2 for Humanoid Robots

### Basic Nav2 Configuration

```yaml
# navigation_params_humanoid.yaml
amcl:
  ros__parameters:
    use_sim_time: True
    alpha1: 0.2
    alpha2: 0.2
    alpha3: 0.2
    alpha4: 0.2
    alpha5: 0.2
    base_frame_id: "base_footprint"
    beam_skip_distance: 0.5
    beam_skip_error_threshold: 0.9
    beam_skip_threshold: 0.3
    do_beamskip: false
    global_frame_id: "map"
    lambda_short: 0.1
    laser_likelihood_max_dist: 2.0
    laser_max_range: 10.0
    laser_min_range: -1.0
    laser_model_type: "likelihood_field"
    max_beams: 60
    max_particles: 2000
    min_particles: 500
    odom_frame_id: "odom"
    pf_err: 0.05
    pf_z: 0.99
    recovery_alpha_fast: 0.0
    recovery_alpha_slow: 0.0
    resample_interval: 1
    robot_model_type: "nav2_amcl::DifferentialMotionModel"
    save_pose_delay: 0.2
    save_pose_rate: 0.5
    sigma_hit: 0.2
    tf_broadcast: true
    transform_tolerance: 1.0
    update_min_a: 0.2
    update_min_d: 0.25
    z_hit: 0.5
    z_max: 0.05
    z_rand: 0.5
    z_short: 0.05

amcl_map_client:
  ros__parameters:
    use_sim_time: True

amcl_rclcpp_node:
  ros__parameters:
    use_sim_time: True

bt_navigator:
  ros__parameters:
    use_sim_time: True
    global_frame: "map"
    robot_frame: "base_link"
    odom_frame: "odom"
    bt_loop_duration: 10
    default_server_timeout: 20
    enable_groot_monitoring: True
    groot_zmq_publisher_port: 1666
    groot_zmq_server_port: 1667
    # Humanoid-specific behavior tree
    plugin_lib_names: ["bt_navigator/ClearEntireCostmapService", 
                       "bt_navigator/GlobalPlannerService", 
                       "bt_navigator/ComputePathToPoseAction", 
                       "bt_navigator/ComputePathThroughPosesAction",
                       "bt_navigator/FollowPathAction",
                       "bt_navigator/BackUpAction",
                       "bt_navigator/SpinAction",
                       "bt_navigator/WaitAction",
                       "bt_navigator/RateController",
                       "bt_navigator/DirectlyTraverseWaypoint",
                       "bt_navigator/IsStuckCondition",
                       "bt_navigator/GoalReachedCondition",
                       "bt_navigator/GoalUpdatedCondition",
                       "bt_navigator/InitialPoseReceivedCondition",
                       "bt_navigator/IsGoalReached",
                       "bt_navigator/IsPathValid",
                       "bt_navigator/IsTaskRunning",
                       "bt_navigator/ReinitializeGlobalLocalizationService",
                       "bt_navigator/TransformAvailableCondition",
                       "bt_navigator/PipelineSequence",
                       "bt_navigator/ModifyPath",
                       "bt_navigator/ComputePathThroughPosesAction",
                       "bt_navigator/TruncatePath",
                       "bt_navigator/SimpleActionCondition",
                       "bt_navigator/ComputeVelocityToPoseAction"]

bt_navigator_rclcpp_node:
  ros__parameters:
    use_sim_time: True

controller_server:
  ros__parameters:
    use_sim_time: True
    controller_frequency: 20.0
    min_x_velocity_threshold: 0.001
    min_y_velocity_threshold: 0.5
    min_theta_velocity_threshold: 0.001
    # Humanoid-specific velocity limits
    progress_checker_plugin: "progress_checker"
    goal_checker_plugin: "goal_checker"
    controller_plugins: ["FollowPath"]

    # Humanoid path follower
    FollowPath:
      plugin: "nav2_mppi_controller::MPPIController"
      time_steps: 50
      model_dt: 0.05
      batch_size: 1000
      vx_std: 0.2
      vy_std: 0.2
      wz_std: 0.3
      vx_max: 0.4  # Slower for humanoid stability
      vx_min: -0.2
      vy_max: 0.2
      wz_max: 0.5
      sim_period: 0.05
      speed_cost_scale: 1.0
      path_alignment_cost_scale: 50.0
      goal_dist_cost_scale: 20.0
      goal_angle_cost_scale: 5.0
      obstacle_cost_scale: 50.0
      constraint_cost_scale: 10.0
      path_angle_cost_scale: 0.0
      reference_speed: 0.3  # Conservative speed for humanoid
      trajector_desv_x_scale: 1.0
      trajector_desv_y_scale: 1.0
      trajector_desv_theta_scale: 0.5
      ctrl_cycle: 0.05
      twirling_cost_scale: 0.0

local_costmap:
  local_costmap:
    ros__parameters:
      update_frequency: 5.0
      publish_frequency: 2.0
      global_frame: "odom"
      robot_base_frame: "base_link"
      use_sim_time: True
      resolution: 0.05  # Higher resolution for precise foot placement
      robot_radius: 0.3  # Humanoid width for collision checking
      plugins: ["voxel_layer", "inflation_layer"]
      inflation_layer:
        plugin: "nav2_costmap_2d::InflationLayer"
        cost_scaling_factor: 3.0
        inflation_radius: 0.55
      voxel_layer:
        plugin: "nav2_costmap_2d::VoxelLayer"
        enabled: True
        publish_voxel_map: True
        origin_z: 0.0
        z_resolution: 0.05
        z_voxels: 16
        max_obstacle_height: 2.0
        mark_threshold: 0
        observation_sources: scan
        scan:
          topic: /scan
          max_obstacle_height: 2.0
          clearing: True
          marking: True
          data_type: "LaserScan"
          raytrace_max_range: 3.0
          raytrace_min_range: 0.0
          obstacle_max_range: 2.5
          obstacle_min_range: 0.0
      static_layer:
        plugin: "nav2_costmap_2d::StaticLayer"
        map_subscribe_transient_local: True
      always_send_full_costmap: True
  local_costmap_client:
    ros__parameters:
      use_sim_time: True
  local_costmap_rclcpp_node:
    ros__parameters:
      use_sim_time: True

global_costmap:
  global_costmap:
    ros__parameters:
      update_frequency: 1.0
      publish_frequency: 1.0
      global_frame: "map"
      robot_base_frame: "base_link"
      use_sim_time: True
      resolution: 0.05
      robot_radius: 0.3  # Match local costmap
      plugins: ["static_layer", "obstacle_layer", "inflation_layer"]
      obstacle_layer:
        plugin: "nav2_costmap_2d::ObstacleLayer"
        enabled: True
        observation_sources: scan
        scan:
          topic: /scan
          max_obstacle_height: 2.0
          clearing: True
          marking: True
          data_type: "LaserScan"
          raytrace_max_range: 3.0
          raytrace_min_range: 0.0
          obstacle_max_range: 2.5
          obstacle_min_range: 0.0
      static_layer:
        plugin: "nav2_costmap_2d::StaticLayer"
        map_subscribe_transient_local: True
      inflation_layer:
        plugin: "nav2_costmap_2d::InflationLayer"
        cost_scaling_factor: 3.0
        inflation_radius: 0.55
      always_send_full_costmap: True
  global_costmap_client:
    ros__parameters:
      use_sim_time: True
  global_costmap_rclcpp_node:
    ros__parameters:
      use_sim_time: True

map_server:
  ros__parameters:
    use_sim_time: True
    yaml_filename: "turtlebot3_world.yaml"

map_saver:
  ros__parameters:
    use_sim_time: True
    save_map_timeout: 5.0
    free_thresh_default: 0.25
    occupied_thresh_default: 0.65

planner_server:
  ros__parameters:
    use_sim_time: True
    planner_plugins: ["GridBased"]
    GridBased:
      # For humanoid robots, we might use a custom planner
      # or configure the generic planner with humanoid constraints
      plugin: "nav2_navfn_planner::NavfnPlanner"
      tolerance: 0.5  # Allow some tolerance for difficult-to-reach goals
      use_astar: false
      allow_unknown: true

smoother_server:
  ros__parameters:
    use_sim_time: True
    smoother_plugins: ["simple_smoother"]
    simple_smoother:
      plugin: "nav2_smoother::SimpleSmoother"
      tolerance: 1.0e-10
      max_its: 1000
      do_refinement: True

behavior_server:
  ros__parameters:
    costmap_topic: "local_costmap/costmap_raw"
    footprint_topic: "local_costmap/published_footprint"
    cycle_frequency: 10.0
    behavior_plugins: ["spin", "backup", "wait"]
    spin:
      plugin: "nav2_behaviors::Spin"
      spin_dist: 1.57  # 90 degrees for turning
    backup:
      plugin: "nav2_behaviors::BackUp"
      backup_dist: 0.15  # Conservative backup distance
      backup_speed: 0.05
    wait:
      plugin: "nav2_behaviors::Wait"
      wait_duration: 1.0

robot_state_publisher:
  ros__parameters:
    use_sim_time: True

waypoint_follower:
  ros__parameters:
    loop_rate: 20
    stop_on_failure: false
    waypoint_task_executor_plugin: "wait_at_waypoint" 
    wait_at_waypoint:
      plugin: "nav2_waypoint_follower::WaitAtWaypoint"
      enabled: true
      wait_time: 1
```

## Humanoid-Specific Path Planning

### Custom Path Planner for Bipedal Robots

```python
from nav2_core.global_planner import GlobalPlanner
from nav2_core.costmap import Costmap2D
from nav2_util import Node
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Path
from builtin_interfaces.msg import Duration
from std_msgs.msg import Header
import numpy as np
import math

class HumanoidPathPlanner(GlobalPlanner):
    def __init__(self):
        super().__init__()
        
    def configure(self, node, name, tf, costmap):
        """Configure the planner with node and costmap"""
        self.node = node
        self.name = name
        self.tf = tf
        self.costmap = costmap
        self.logger = node.get_logger()
        
        # Humanoid-specific parameters
        self.step_length = 0.3  # Maximum step length in meters
        self.step_width = 0.2   # Width for foot placement
        self.turn_radius = 0.4  # Minimum turning radius
        
        self.logger.info(f"{self.name} planner configured")

    def cleanup(self):
        """Cleanup the planner"""
        self.logger.info(f"{self.name} planner cleaned up")

    def set_costmap(self, costmap):
        """Set the costmap for the planner"""
        self.costmap = costmap

    def create_plan(self, start, goal):
        """Create a path plan for a humanoid robot"""
        self.logger.info(f"Creating plan from ({start.pose.position.x}, {start.pose.position.y}) "
                        f"to ({goal.pose.position.x}, {goal.pose.position.y})")
        
        # Check if start and goal are in valid areas
        if not self.is_valid_pose(start) or not self.is_valid_pose(goal):
            self.logger.warn("Start or goal pose is invalid")
            return Path()
        
        # Calculate path using A* or Dijkstra's algorithm adapted for humanoid
        path = self.calculate_humanoid_path(start, goal)
        
        return path

    def is_valid_pose(self, pose):
        """Check if a pose is valid for humanoid navigation"""
        # Convert pose to costmap coordinates
        costmap = self.costmap.get_costmap()
        mx, my = self.pose_to_costmap_coords(pose)
        
        # Check if pose is within map bounds
        if mx < 0 or mx >= costmap.get_size_x() or my < 0 or my >= costmap.get_size_y():
            return False
        
        # Check cost at location (must be less than lethal obstacle cost)
        cost = costmap.get_cost(mx, my)
        return cost != 254  # LETHAL_OBSTACLE cost in Nav2

    def pose_to_costmap_coords(self, pose):
        """Convert pose to costmap coordinates"""
        costmap = self.costmap.get_costmap()
        origin_x = costmap.get_origin_x()
        origin_y = costmap.get_origin_y()
        resolution = costmap.get_resolution()
        
        mx = int((pose.pose.position.x - origin_x) / resolution)
        my = int((pose.pose.position.y - origin_y) / resolution)
        
        return mx, my

    def calculate_humanoid_path(self, start, goal):
        """Calculate a path that considers humanoid constraints"""
        # Initialize path
        path = Path()
        path.header = Header()
        path.header.stamp = self.node.get_clock().now().to_msg()
        path.header.frame_id = "map"
        
        # For simplicity, implement a grid-based path with humanoid constraints
        # In practice, you'd implement a more sophisticated algorithm
        
        # Calculate the straight-line path first
        dx = goal.pose.position.x - start.pose.position.x
        dy = goal.pose.position.y - start.pose.position.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        # Create intermediate poses with appropriate spacing for humanoid steps
        steps = int(distance / self.step_length) + 1
        step_size = distance / steps if steps > 0 else 0
        
        if steps > 0:
            for i in range(steps + 1):
                t = i / steps if steps > 0 else 0
                pose = PoseStamped()
                pose.header = path.header
                pose.pose.position.x = start.pose.position.x + t * dx
                pose.pose.position.y = start.pose.position.y + t * dy
                pose.pose.position.z = start.pose.position.z  # Maintain height
                
                # Set orientation to face the direction of travel
                if i < steps:
                    next_x = start.pose.position.x + (i+1)/steps * dx
                    next_y = start.pose.position.y + (i+1)/steps * dy
                    yaw = math.atan2(next_y - pose.pose.position.y, 
                                   next_x - pose.pose.position.x)
                    
                    # Convert yaw to quaternion
                    cy = math.cos(yaw * 0.5)
                    sy = math.sin(yaw * 0.5)
                    pose.pose.orientation.z = sy
                    pose.pose.orientation.w = cy
                
                path.poses.append(pose)
        
        # Add the goal position at the end to ensure we reach it
        if path.poses:
            final_pose = PoseStamped()
            final_pose.header = path.header
            final_pose.pose = goal.pose
            path.poses[-1] = final_pose  # Replace last calculated pose with exact goal
        
        return path

def register_plugins():
    """Register the humanoid path planner plugin"""
    return HumanoidPathPlanner()
```

## Creating a Behavior Tree for Humanoid Navigation

### Custom Behavior Tree for Bipedal Locomotion

```xml
<!-- humanoid_navigation_tree.xml -->
<root main_tree_to_execute="MainTree">
    <BehaviorTree ID="MainTree">
        <PipelineSequence name="NavigateWithRecovery">
            <RecoveryNode number_of_retries="4" name="SpinAndBackup">
                <Sequence name="SpinOrBackup">
                    <IsStuckCondition/>
                    <ReactiveFallback name="SpinOrBackupFallback">
                        <Spin spin_dist="1.57" name="Spin"/>
                        <BackUp backup_dist="0.3" backup_speed="0.1" name="BackUp"/>
                    </ReactiveFallback>
                </Sequence>
            </RecoveryNode>
            
            <Sequence name="ComputeAndFollowPath">
                <GoalUpdatedCondition/>
                <ComputePathToPose goal="current_goal" path="path" planner_id="GridBased"/>
                <TruncatePath distance="1.0" input_path="path" output_path="truncated_path"/>
                <FollowPath path="truncated_path" controller_id="FollowPath"/>
            </Sequence>
        </PipelineSequence>
    </BehaviorTree>
</root>
```

## Footstep Planning Integration

### Connecting Navigation to Footstep Planning

```python
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped, Twist
from nav_msgs.msg import Path
from std_msgs.msg import Bool
import numpy as np
import math

class HumanoidFootstepPlanner(Node):
    def __init__(self):
        super().__init__('humanoid_footstep_planner')
        
        # Subscribe to navigation path
        self.path_sub = self.create_subscription(
            Path,
            '/plan',
            self.path_callback,
            10
        )
        
        # Publish footstep commands
        self.footstep_pub = self.create_publisher(
            Path,
            '/footsteps',
            10
        )
        
        # Subscribe to robot state
        self.state_sub = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.state_callback,
            10
        )
        
        # Timer for footstep generation
        self.timer = self.create_timer(0.1, self.generate_footsteps)
        
        # Robot parameters
        self.step_length = 0.3  # m
        self.step_width = 0.2   # m (distance between feet)
        self.max_step_height = 0.05  # m
        
        # Internal state
        self.current_path = None
        self.current_idx = 0
        self.robot_pose = None
        self.left_foot = True  # Start with left foot
        
        self.get_logger().info("Humanoid Footstep Planner initialized")

    def path_callback(self, msg):
        """Receive navigation path and convert to footsteps"""
        self.current_path = msg
        self.current_idx = 0
        self.get_logger().info(f"Received path with {len(msg.poses)} waypoints")

    def state_callback(self, msg):
        """Update robot state"""
        # In a real implementation, this would update the robot's actual position
        pass

    def generate_footsteps(self):
        """Generate footsteps based on the current path"""
        if self.current_path is None or self.current_idx >= len(self.current_path.poses):
            return
            
        # Create path of footsteps
        footsteps = Path()
        footsteps.header = self.current_path.header
        
        # Calculate footsteps along the path
        path_segment = self.current_path.poses[self.current_idx:]
        
        # Generate footsteps at appropriate intervals
        step_interval = self.step_length * 0.8  # Slightly less than full step for overlap
        cumulative_distance = 0
        
        for i in range(len(path_segment) - 1):
            current_pose = path_segment[i].pose.position
            next_pose = path_segment[i+1].pose.position
            
            # Calculate distance between poses
            dx = next_pose.x - current_pose.x
            dy = next_pose.y - current_pose.y
            segment_distance = math.sqrt(dx*dx + dy*dy)
            
            cumulative_distance += segment_distance
            
            # Create a step when we've moved enough
            if cumulative_distance >= step_interval:
                foot_pose = PoseStamped()
                foot_pose.header = footsteps.header
                foot_pose.pose.position.x = next_pose.x
                foot_pose.pose.position.y = next_pose.y
                foot_pose.pose.position.z = 0.0  # Ground level
                
                # Adjust for left/right foot alternation
                if self.left_foot:
                    foot_pose.pose.position.y += self.step_width / 2
                else:
                    foot_pose.pose.position.y -= self.step_width / 2
                
                # Set orientation to match path direction
                yaw = math.atan2(dy, dx)
                cy = math.cos(yaw * 0.5)
                sy = math.sin(yaw * 0.5)
                foot_pose.pose.orientation.z = sy
                foot_pose.pose.orientation.w = cy
                
                footsteps.poses.append(foot_pose)
                cumulative_distance = 0
                self.left_foot = not self.left_foot  # Alternate feet
                
                # Increase path index to continue tracking progress
                self.current_idx += 1
                
                # Limit to prevent excessive footsteps
                if len(footsteps.poses) >= 10:  # Plan 10 steps ahead
                    break
        
        # Publish the footsteps
        if len(footsteps.poses) > 0:
            self.footstep_pub.publish(footsteps)
            self.get_logger().info(f"Published {len(footsteps.poses)} footsteps")

def main(args=None):
    rclpy.init(args=args)
    node = HumanoidFootstepPlanner()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
```

## Integration with Gait Controllers

### Connecting Navigation to Gait Control

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist, PoseStamped
from sensor_msgs.msg import JointState
import math

class HumanoidGaitController(Node):
    def __init__(self):
        super().__init__('humanoid_gait_controller')
        
        # Subscribe to navigation commands
        self.nav_cmd_sub = self.create_subscription(
            Twist,
            '/cmd_vel_nav',  # Navigation-level velocity commands
            self.nav_cmd_callback,
            10
        )
        
        # Subscribe to footstep plans
        self.footstep_sub = self.create_subscription(
            PoseStamped,
            '/next_footstep',
            self.footstep_callback,
            10
        )
        
        # Publish joint commands
        self.joint_cmd_pub = self.create_publisher(
            JointState,
            '/joint_commands',
            10
        )
        
        # Timer for gait execution
        self.timer = self.create_timer(0.02, self.execute_gait)  # 50Hz control loop
        
        # Gait parameters
        self.step_height = 0.05  # m
        self.step_duration = 0.8  # s
        self.nominal_height = 0.8  # m (height of robot at hip level)
        
        # Gait state
        self.gait_phase = 0.0  # 0.0 to 1.0
        self.gait_state = 'STANCE'  # STANCE, LIFT, SWING, PLACE
        self.left_support = True  # Start with left foot support
        
        self.get_logger().info("Humanoid Gait Controller initialized")

    def nav_cmd_callback(self, msg):
        """Receive navigation velocity commands and generate gait parameters"""
        # Convert navigation commands to gait parameters
        self.desired_forward_speed = msg.linear.x
        self.desired_turn_rate = msg.angular.z
        
        # Adjust gait parameters based on desired speed
        if abs(self.desired_forward_speed) > 0.01:
            # Adjust step parameters based on desired speed
            self.step_length = min(0.4, max(0.1, 0.2 + 0.3 * abs(self.desired_forward_speed)))
            self.step_duration = max(0.5, 0.8 - 0.2 * abs(self.desired_forward_speed))
        else:
            self.step_length = 0.2
            self.step_duration = 0.8

    def footstep_callback(self, msg):
        """Receive next footstep location"""
        # In a real implementation, this would plan footsteps based on
        # the footstep location from the footstep planner
        pass

    def execute_gait(self):
        """Execute the current gait phase"""
        # Update gait phase
        dt = 0.02  # Timer period
        phase_increment = dt / self.step_duration
        self.gait_phase = (self.gait_phase + phase_increment) % 1.0
        
        # Determine gait state based on phase
        if self.gait_phase < 0.1:
            self.gait_state = 'PLACE'
        elif self.gait_phase < 0.5:
            self.gait_state = 'STANCE'
        elif self.gait_phase < 0.6:
            self.gait_state = 'LIFT'
        else:
            self.gait_state = 'SWING'
        
        # Generate joint commands based on gait state
        joint_commands = self.compute_joint_commands()
        self.publish_joint_commands(joint_commands)

    def compute_joint_commands(self):
        """Compute desired joint positions for current gait phase"""
        # Simplified gait model - in practice, this would use inverse kinematics
        joint_state = JointState()
        joint_state.header.stamp = self.get_clock().now().to_msg()
        joint_state.name = [
            'left_hip_roll', 'left_hip_pitch', 'left_knee',
            'right_hip_roll', 'right_hip_pitch', 'right_knee',
            'left_ankle_pitch', 'right_ankle_pitch'
        ]
        
        # Calculate joint positions based on gait phase
        if self.gait_state == 'STANCE':
            # Both feet on ground, supporting body
            joint_positions = [0.0, 0.1, -0.2, 0.0, 0.1, -0.2, 0.0, 0.0]
        elif self.gait_state == 'LIFT':
            # Lifting swing foot
            if self.left_support:
                joint_positions = [0.0, 0.1, -0.2, 0.0, 0.2, -0.3, 0.0, 0.0]  # Raise right knee
            else:
                joint_positions = [0.0, 0.2, -0.3, 0.0, 0.1, -0.2, 0.0, 0.0]  # Raise left knee
        elif self.gait_state == 'SWING':
            # Swinging foot forward
            if self.left_support:
                # Move right foot forward
                joint_positions = [0.0, 0.0, -0.1, 0.0, 0.0, -0.1, 0.0, 0.0]
            else:
                # Move left foot forward
                joint_positions = [0.0, 0.0, -0.1, 0.0, 0.0, -0.1, 0.0, 0.0]
        else:  # PLACE
            # Placing foot down
            joint_positions = [0.0, 0.1, -0.2, 0.0, 0.1, -0.2, 0.0, 0.0]
        
        joint_state.position = joint_positions
        return joint_state

    def publish_joint_commands(self, joint_state):
        """Publish joint commands to robot"""
        self.joint_cmd_pub.publish(joint_state)

def main(args=None):
    rclpy.init(args=args)
    node = HumanoidGaitController()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
```

## Optimizing Navigation for Humanoid Constraints

### Balancing and Stability Considerations

```python
class HumanoidNavigationOptimizer:
    def __init__(self):
        # Stability parameters
        self.compliance_factor = 0.1  # How much to smooth the path
        self.look_ahead_distance = 0.5  # m
        self.max_angular_velocity = 0.3  # rad/s (limited for balance)
        self.min_turn_radius = 0.4  # m
        
    def optimize_path_for_humanoid(self, original_path):
        """Apply humanoid-specific optimizations to a path"""
        if len(original_path.poses) < 2:
            return original_path
            
        optimized_path = Path()
        optimized_path.header = original_path.header
        
        # Add first point
        optimized_path.poses.append(original_path.poses[0])
        
        # Smooth the path to reduce sharp turns
        smoothed_poses = self.smooth_path(original_path.poses)
        
        # Add smoothed points
        for pose in smoothed_poses[1:]:  # Skip first to avoid duplication
            optimized_path.poses.append(pose)
            
        return optimized_path
    
    def smooth_path(self, poses):
        """Apply smoothing to reduce sharp direction changes"""
        if len(poses) < 3:
            return poses
            
        smoothed = [poses[0]]  # Start with first pose
        
        for i in range(1, len(poses) - 1):
            prev_pos = np.array([poses[i-1].pose.position.x, poses[i-1].pose.position.y])
            curr_pos = np.array([poses[i].pose.position.x, poses[i].pose.position.y])
            next_pos = np.array([poses[i+1].pose.position.x, poses[i+1].pose.position.y])
            
            # Calculate smoothed position
            smoothed_pos = (prev_pos + 2*curr_pos + next_pos) / 4
            
            # Create new pose with smoothed position
            new_pose = PoseStamped()
            new_pose.header = poses[i].header
            new_pose.pose.position.x = smoothed_pos[0]
            new_pose.pose.position.y = smoothed_pos[1]
            new_pose.pose.position.z = poses[i].pose.position.z  # Keep original z
            
            # Preserve orientation or calculate based on direction
            if i < len(poses) - 1:
                dx = poses[i+1].pose.position.x - poses[i-1].pose.position.x
                dy = poses[i+1].pose.position.y - poses[i-1].pose.position.y
                yaw = math.atan2(dy, dx)
                cy = math.cos(yaw * 0.5)
                sy = math.sin(yaw * 0.5)
                new_pose.pose.orientation.z = sy
                new_pose.pose.orientation.w = cy
            else:
                new_pose.pose.orientation = poses[i].pose.orientation
                
            smoothed.append(new_pose)
        
        # Add last pose
        smoothed.append(poses[-1])
        
        return smoothed
```

## Best Practices for Humanoid Navigation

### Path Planning Considerations

1. **Step Feasibility**: Ensure planned paths account for the robot's step constraints
2. **Dynamic Balance**: Plan paths that maintain the robot's center of mass within its support polygon
3. **Turning Radius**: Account for the humanoid's limited turning capabilities
4. **Terrain Adaptation**: Consider different locomotion modes for stairs, slopes, and uneven terrain
5. **Recovery Behaviors**: Implement appropriate recovery behaviors for humanoid-specific failure modes

### Performance Optimization

1. **Path Resolution**: Use appropriate path resolution that matches the humanoid's step size
2. **Computational Efficiency**: Optimize algorithms for real-time performance
3. **Sensor Fusion**: Combine multiple sensor modalities for robust navigation
4. **Safety Margins**: Include appropriate safety margins in path planning

By properly configuring Nav2 with humanoid-specific parameters and integrating with gait controllers, you can enable humanoid robots to navigate complex environments safely and efficiently. The combination of global path planning and local footstep planning allows for robust bipedal navigation.