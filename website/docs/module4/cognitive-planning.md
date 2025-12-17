---
sidebar_position: 3
title: Cognitive Planning - Using LLMs to Translate Natural Language into ROS 2 Actions
---

# Cognitive Planning: Using LLMs to Translate Natural Language into ROS 2 Actions

## Introduction to LLM-Based Cognitive Planning

Cognitive planning in robotics involves the high-level reasoning required to transform natural language commands into executable robot behaviors. Large Language Models (LLMs) excel at this task by providing natural language understanding, commonsense reasoning, and the ability to decompose complex tasks into simpler, executable steps. This integration enables robots to interpret human instructions in a natural, flexible way.

## Architecture of LLM-Based Cognitive Planning

The cognitive planning system typically involves:

1. **Command Interpretation**: Understanding the user's natural language request
2. **Task Decomposition**: Breaking down the command into specific, actionable steps
3. **Environment Understanding**: Relating the command to the robot's current environment
4. **Action Planning**: Generating a sequence of ROS 2-compatible actions
5. **Execution Monitoring**: Tracking and adapting the plan as needed

## Setting Up OpenAI Integration

### Basic LLM Integration Node

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Path
import openai
import json
import time

class CognitivePlannerNode(Node):
    def __init__(self):
        super().__init__('cognitive_planner_node')
        
        # Initialize OpenAI API key (should be set in environment or config)
        openai.api_key = "your-api-key-here"  # In practice, get from secure config
        
        # Set up model to use
        self.model_name = "gpt-3.5-turbo"  # or "gpt-4" for more complex reasoning
        
        # Subscribers
        self.command_sub = self.create_subscription(
            String,
            '/natural_language_command',
            self.command_callback,
            10
        )
        
        # Publishers
        self.action_pub = self.create_publisher(
            String,
            '/planned_actions',
            10
        )
        
        self.get_logger().info("Cognitive Planner Node initialized")

    def command_callback(self, msg):
        """Process natural language command and generate plan"""
        try:
            command = msg.data
            
            # Generate a plan using the LLM
            plan = self.generate_plan(command)
            
            if plan:
                # Publish the plan as a JSON string
                plan_msg = String()
                plan_msg.data = json.dumps(plan)
                self.action_pub.publish(plan_msg)
                
                self.get_logger().info(f"Generated plan: {plan}")
            else:
                self.get_logger().warn(f"Could not generate plan for command: {command}")
                
        except Exception as e:
            self.get_logger().error(f"Error in command processing: {e}")

    def generate_plan(self, command):
        """Generate a plan for the given command using an LLM"""
        # Define the system prompt to guide the LLM
        system_prompt = """
        You are a helpful assistant that converts natural language robot commands into structured action plans.
        The robot is a humanoid robot capable of navigation, object manipulation, and interaction with the environment.
        Convert the user's request into a sequence of specific actions that the robot can execute.
        
        Available actions:
        - navigate_to: Move the robot to a specific location
        - detect_object: Identify objects in the environment
        - pick_up: Grasp an object
        - place: Place an object at a location
        - open: Open doors, containers, etc.
        - close: Close doors, containers, etc.
        - turn_on: Activate a device
        - turn_off: Deactivate a device
        - speak: Make the robot speak a response
        
        Respond in valid JSON format with the following structure:
        {
          "command": "original_command",
          "actions": [
            {
              "action": "action_name",
              "parameters": {
                "target": "object or location",
                "location": "specific_location"
              }
            }
          ]
        }
        
        Be specific about locations and objects. If a location or object is not specified, 
        you may need to ask for clarification or use the default values.
        """
        
        try:
            response = openai.ChatCompletion.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Command: {command}"}
                ],
                temperature=0.3,  # Lower temperature for more consistent outputs
                max_tokens=500
            )
            
            # Extract and parse the response
            response_text = response.choices[0].message['content'].strip()
            
            # Sometimes the LLM includes markdown formatting, so strip it
            if response_text.startswith("```json"):
                response_text = response_text[7:]  # Remove ```json
            if response_text.endswith("```"):
                response_text = response_text[:-3]  # Remove ```
            
            plan = json.loads(response_text)
            return plan
            
        except json.JSONDecodeError:
            self.get_logger().error(f"Could not parse LLM response as JSON: {response_text}")
            return None
        except Exception as e:
            self.get_logger().error(f"Error calling LLM: {e}")
            return None

def main(args=None):
    rclpy.init(args=args)
    node = CognitivePlannerNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
```

## Advanced Cognitive Planning with Context Awareness

### Context-Aware Planning Node

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped, Point
from sensor_msgs.msg import Image
from visualization_msgs.msg import MarkerArray
import openai
import json
import time
from typing import Dict, List, Any

class ContextAwareCognitivePlanner(Node):
    def __init__(self):
        super().__init__('context_aware_cognitive_planner')
        
        # Initialize OpenAI API
        openai.api_key = "your-api-key-here"  # In practice, get from secure config
        self.model_name = "gpt-4"  # Use GPT-4 for better reasoning
        
        # Subscribers
        self.command_sub = self.create_subscription(
            String,
            '/natural_language_command',
            self.command_callback,
            10
        )
        
        self.robot_pose_sub = self.create_subscription(
            PoseStamped,
            '/robot_pose',
            self.pose_callback,
            10
        )
        
        self.object_detection_sub = self.create_subscription(
            MarkerArray,
            '/detected_objects',
            self.object_detection_callback,
            10
        )
        
        # Publishers
        self.action_pub = self.create_publisher(
            String,
            '/contextual_planned_actions',
            10
        )
        
        self.get_logger().info("Context-Aware Cognitive Planner initialized")
        
        # Context storage
        self.robot_pose = None
        self.detected_objects = {}
        self.room_layout = {}  # Could store known locations of furniture, etc.

    def pose_callback(self, msg):
        """Update robot's pose in the context"""
        self.robot_pose = {
            'x': msg.pose.position.x,
            'y': msg.pose.position.y,
            'z': msg.pose.position.z,
            'orientation': {
                'x': msg.pose.orientation.x,
                'y': msg.pose.orientation.y,
                'z': msg.pose.orientation.z,
                'w': msg.pose.orientation.w
            }
        }

    def object_detection_callback(self, msg):
        """Update detected objects in the environment"""
        self.detected_objects = {}
        for marker in msg.markers:
            self.detected_objects[marker.ns] = {
                'id': marker.id,
                'name': marker.ns,
                'position': {
                    'x': marker.pose.position.x,
                    'y': marker.pose.position.y,
                    'z': marker.pose.position.z
                },
                'type': marker.type  # Can distinguish between different object types
            }

    def command_callback(self, msg):
        """Process command with environmental context"""
        try:
            command = msg.data
            
            # Generate plan with context
            plan = self.generate_contextual_plan(command)
            
            if plan:
                plan_msg = String()
                plan_msg.data = json.dumps(plan)
                self.action_pub.publish(plan_msg)
                
                self.get_logger().info(f"Generated contextual plan: {plan}")
            else:
                self.get_logger().warn(f"Could not generate plan for command: {command}")
                
        except Exception as e:
            self.get_logger().error(f"Error in contextual command processing: {e}")

    def generate_contextual_plan(self, command):
        """Generate a plan considering environmental context"""
        # Create contextual prompt
        context = self.get_environment_context()
        
        system_prompt = f"""
        You are a helpful assistant that converts natural language robot commands into structured action plans.
        The robot is a humanoid robot operating in the following environment:
        
        {context}
        
        The robot has the following capabilities:
        - Navigation: Can move to specified coordinates
        - Object Detection: Can identify and locate objects in the environment
        - Manipulation: Can pick up and place objects
        - Interaction: Can open/close doors, turn devices on/off
        
        Convert the user's request into a sequence of specific actions that the robot can execute.
        
        Available actions:
        - navigate_to: Move to a specific location (x, y, z coordinates)
        - detect_object: Search for a specific object
        - pick_up: Grasp an object at given coordinates
        - place: Place an object at coordinates
        - open: Open doors, containers, etc.
        - close: Close doors, containers, etc.
        - turn_on: Activate a device
        - turn_off: Deactivate a device
        - speak: Make the robot speak a response
        
        Respond in valid JSON format:
        {{
          "command": "original_command",
          "actions": [
            {{
              "action": "action_name",
              "parameters": {{
                "target": "object or location",
                "coordinates": [x, y, z]  // Include if navigation/movement required
              }}
            }}
          ]
        }}
        
        Consider the robot's current location and the locations of objects when generating the plan.
        Optimize for efficiency and safety.
        """
        
        try:
            response = openai.ChatCompletion.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Command: {command}"}
                ],
                temperature=0.3,
                max_tokens=800
            )
            
            response_text = response.choices[0].message['content'].strip()
            
            # Clean up markdown formatting
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            
            plan = json.loads(response_text)
            return plan
            
        except json.JSONDecodeError:
            self.get_logger().error(f"Could not parse LLM response as JSON: {response_text}")
            return None
        except Exception as e:
            self.get_logger().error(f"Error calling LLM: {e}")
            return None

    def get_environment_context(self):
        """Generate a text representation of the current environment"""
        context_parts = []
        
        # Robot's current position
        if self.robot_pose:
            context_parts.append(
                f"Robot is currently at position (x={self.robot_pose['x']:.2f}, "
                f"y={self.robot_pose['y']:.2f}, z={self.robot_pose['z']:.2f})"
            )
        
        # Detected objects
        if self.detected_objects:
            obj_descriptions = []
            for name, obj_data in self.detected_objects.items():
                obj_descriptions.append(
                    f"{name} at (x={obj_data['position']['x']:.2f}, "
                    f"y={obj_data['position']['y']:.2f}, z={obj_data['position']['z']:.2f})"
                )
            context_parts.append(f"Detected objects: {', '.join(obj_descriptions)}")
        
        # Known room layout (if available)
        if self.room_layout:
            room_descriptions = [f"{name}: {location}" for name, location in self.room_layout.items()]
            context_parts.append(f"Room layout: {', '.join(room_descriptions)}")
        
        return "\n".join(context_parts)

def main(args=None):
    rclpy.init(args=args)
    node = ContextAwareCognitivePlanner()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
```

## Task Decomposition and Execution Planning

### Advanced Planning with Task Dependencies

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from action_msgs.msg import GoalStatus
import openai
import json
from typing import List, Dict
import time

class AdvancedCognitivePlanner(Node):
    def __init__(self):
        super().__init__('advanced_cognitive_planner')
        
        # Initialize OpenAI API
        openai.api_key = "your-api-key-here"
        self.model_name = "gpt-4"
        
        # Subscribers and publishers
        self.command_sub = self.create_subscription(
            String,
            '/high_level_command',
            self.command_callback,
            10
        )
        
        self.action_status_sub = self.create_subscription(
            String,
            '/action_status',
            self.action_status_callback,
            10
        )
        
        self.decomposed_action_pub = self.create_publisher(
            String,
            '/decomposed_actions',
            10
        )
        
        self.get_logger().info("Advanced Cognitive Planner initialized")
        
        # Store active plans
        self.active_plans = {}
        self.plan_id_counter = 0

    def command_callback(self, msg):
        """Process high-level command and create detailed plan"""
        try:
            command = msg.data
            plan_id = f"plan_{self.plan_id_counter}"
            self.plan_id_counter += 1
            
            # Generate detailed plan using LLM
            plan = self.generate_detailed_plan(command, plan_id)
            
            if plan:
                # Store the plan
                self.active_plans[plan_id] = {
                    'plan': plan,
                    'current_step': 0,
                    'status': 'active',
                    'start_time': time.time()
                }
                
                # Publish first action
                self.publish_next_action(plan_id)
                
                self.get_logger().info(f"Started plan {plan_id}: {plan}")
            else:
                self.get_logger().warn(f"Could not generate plan for command: {command}")
                
        except Exception as e:
            self.get_logger().error(f"Error in advanced command processing: {e}")

    def generate_detailed_plan(self, command, plan_id):
        """Generate a detailed, step-by-step plan with dependencies"""
        system_prompt = """
        You are an expert in robotic task planning. Convert the user's command into a detailed plan 
        with specific, executable steps for a humanoid robot. Consider:
        
        1. Pre-conditions: What must be true before each step
        2. Post-conditions: What will be true after each step
        3. Dependencies: Which steps must be completed before others can begin
        4. Expected duration: Approximately how long each step will take
        5. Success/failure criteria: How to determine if each step succeeded
        
        The robot has the following capabilities:
        - Navigation: Move to specific locations
        - Perception: Detect objects, people, and obstacles
        - Manipulation: Pick up, move, and place objects
        - Interaction: Operate switches, doors, and devices
        
        Available primitive actions:
        - move_to: Navigate to a location
        - detect: Find a specific object
        - grasp: Pick up an object
        - release: Place an object
        - operate: Use a device or control
        - wait: Pause for a specified time
        - check: Verify a condition
        
        Respond in JSON format:
        {
          "plan_id": "unique_identifier",
          "original_command": "original user command",
          "steps": [
            {
              "id": "step_1",
              "description": "What this step does",
              "action": "primitive_action",
              "parameters": {
                "target": "object or location",
                "coordinates": [x, y, z]  // if navigation required
              },
              "preconditions": ["condition1", "condition2"],
              "postconditions": ["condition1", "condition2"],
              "dependencies": ["step_id1", "step_id2"],  // IDs of steps that must complete first
              "estimated_duration": 5.0  // in seconds
            }
          ]
        }
        
        Make sure the plan is executable and realistic for a humanoid robot.
        """
        
        try:
            response = openai.ChatCompletion.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Command: {command}"}
                ],
                temperature=0.2,
                max_tokens=1000
            )
            
            response_text = response.choices[0].message['content'].strip()
            
            # Clean up markdown formatting
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            
            plan = json.loads(response_text)
            return plan
            
        except json.JSONDecodeError:
            self.get_logger().error(f"Could not parse LLM response as JSON: {response_text}")
            return None
        except Exception as e:
            self.get_logger().error(f"Error calling LLM: {e}")
            return None

    def action_status_callback(self, msg):
        """Handle action completion status"""
        try:
            status_data = json.loads(msg.data)
            plan_id = status_data.get('plan_id')
            step_id = status_data.get('step_id')
            status = status_data.get('status')  # success, failure, in_progress
            
            if plan_id in self.active_plans:
                plan_info = self.active_plans[plan_id]
                
                if status == 'success':
                    # Move to next step
                    plan_info['current_step'] += 1
                    
                    if plan_info['current_step'] < len(plan_info['plan']['steps']):
                        # Execute next action
                        self.publish_next_action(plan_id)
                    else:
                        # Plan completed
                        plan_info['status'] = 'completed'
                        self.get_logger().info(f"Plan {plan_id} completed successfully")
                        
                elif status == 'failure':
                    # Handle failure - could try alternative approach
                    plan_info['status'] = 'failed'
                    self.get_logger().error(f"Plan {plan_id} failed at step {step_id}")
                    
        except Exception as e:
            self.get_logger().error(f"Error processing action status: {e}")

    def publish_next_action(self, plan_id):
        """Publish the next action in the plan"""
        plan_info = self.active_plans[plan_id]
        current_step = plan_info['current_step']
        
        if current_step < len(plan_info['plan']['steps']):
            step = plan_info['plan']['steps'][current_step]
            
            # Prepare action message
            action_msg = {
                'plan_id': plan_id,
                'step_id': f"step_{current_step}",
                'action': step['action'],
                'parameters': step['parameters'],
                'step_description': step['description']
            }
            
            # Publish the action
            action_msg_str = String()
            action_msg_str.data = json.dumps(action_msg)
            self.decomposed_action_pub.publish(action_msg_str)
            
            self.get_logger().info(f"Published action for plan {plan_id}, step {current_step}: {step['description']}")

def main(args=None):
    rclpy.init(args=args)
    node = AdvancedCognitivePlanner()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
```

## Integration with ROS 2 Action Servers

### Cognitive Planner with Action Server Integration

```python
import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped
import openai
import json
from threading import Thread

# Define a custom action for cognitive planning
from rclpy.action import ActionClient
from your_package.action import PlanAndExecute  # This would be defined in your package

class CognitivePlanningActionServer(Node):
    def __init__(self):
        super().__init__('cognitive_planning_action_server')
        
        # Initialize OpenAI API
        openai.api_key = "your-api-key-here"
        self.model_name = "gpt-4"
        
        # Create action server
        self._action_server = ActionServer(
            self,
            PlanAndExecute,
            'plan_and_execute',
            self.execute_callback
        )
        
        # Publishers for internal communication
        self.command_pub = self.create_publisher(
            String,
            '/cognitive_command',
            10
        )
        
        self.get_logger().info("Cognitive Planning Action Server initialized")

    async def execute_callback(self, goal_handle):
        """Execute the planning and execution goal"""
        self.get_logger().info('Executing plan and execute goal')
        
        feedback_msg = PlanAndExecute.Feedback()
        result = PlanAndExecute.Result()
        
        command = goal_handle.request.command
        self.get_logger().info(f'Received command: {command}')
        
        # Update feedback
        feedback_msg.status = "Generating plan..."
        goal_handle.publish_feedback(feedback_msg)
        
        # Generate plan using LLM
        plan = self.generate_plan_with_llm(command)
        
        if not plan:
            result.success = False
            result.message = "Failed to generate plan"
            goal_handle.succeed()
            return result
        
        # Execute the plan step by step
        feedback_msg.status = "Executing plan..."
        goal_handle.publish_feedback(feedback_msg)
        
        success = self.execute_plan(plan, goal_handle, feedback_msg)
        
        result.success = success
        result.message = f"Plan execution {'succeeded' if success else 'failed'}"
        
        if success:
            goal_handle.succeed()
        else:
            goal_handle.abort()
            
        return result

    def generate_plan_with_llm(self, command):
        """Generate a plan using the LLM"""
        system_prompt = """
        You are a helpful assistant that converts natural language robot commands into detailed execution plans.
        The robot is a humanoid with navigation, manipulation, and interaction capabilities.
        
        Provide the plan in the following JSON format:
        {
          "original_command": "user's command",
          "intention": "what the user wants to achieve",
          "plan": [
            {
              "step": 1,
              "action": "action_type",
              "description": "what to do in this step",
              "parameters": {
                "target": "target object or location",
                "coordinates": [x, y, z]  // if navigation needed
              }
            }
          ]
        }
        """
        
        try:
            response = openai.ChatCompletion.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Command: {command}"}
                ],
                temperature=0.3,
                max_tokens=800
            )
            
            response_text = response.choices[0].message['content'].strip()
            
            # Clean up markdown formatting
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            
            return json.loads(response_text)
            
        except Exception as e:
            self.get_logger().error(f"Error generating plan with LLM: {e}")
            return None

    def execute_plan(self, plan, goal_handle, feedback_msg):
        """Execute the generated plan"""
        steps = plan.get('plan', [])
        
        for i, step in enumerate(steps):
            # Update feedback
            feedback_msg.status = f"Executing step {i+1}/{len(steps)}: {step.get('description', 'Unknown')}"
            feedback_msg.progress = float(i+1) / len(steps) * 100.0
            goal_handle.publish_feedback(feedback_msg)
            
            # Execute the action
            success = self.execute_single_step(step)
            
            if not success:
                self.get_logger().error(f"Failed to execute step {i+1}: {step}")
                return False
            
            # Small delay between steps
            time.sleep(0.1)
        
        return True

    def execute_single_step(self, step):
        """Execute a single step of the plan"""
        action = step.get('action', '')
        parameters = step.get('parameters', {})
        
        # In a real implementation, this would call specific ROS 2 services or actions
        # based on the action type and parameters
        
        self.get_logger().info(f"Executing action: {action} with parameters: {parameters}")
        
        # This is a simplified simulation - in practice, you would
        # call the appropriate ROS 2 service or action for each type
        if action == 'navigate_to':
            return self.navigate_to_location(parameters.get('coordinates'))
        elif action == 'pick_up':
            return self.pick_up_object(parameters.get('target'))
        elif action == 'place':
            return self.place_object(parameters.get('target'))
        elif action == 'detect':
            return self.detect_object(parameters.get('target'))
        else:
            self.get_logger().warn(f"Unknown action type: {action}")
            return False

    def navigate_to_location(self, coordinates):
        """Navigate to the specified location"""
        # Implementation would call navigation service
        self.get_logger().info(f"Navigating to {coordinates}")
        return True  # Simplified; would check actual navigation result

    def pick_up_object(self, target):
        """Pick up the specified object"""
        # Implementation would call manipulation service
        self.get_logger().info(f"Attempting to pick up {target}")
        return True  # Simplified; would check actual manipulation result

    def place_object(self, target):
        """Place the object at the specified location"""
        # Implementation would call manipulation service
        self.get_logger().info(f"Attempting to place {target}")
        return True  # Simplified; would check actual manipulation result

    def detect_object(self, target):
        """Detect the specified object"""
        # Implementation would call perception service
        self.get_logger().info(f"Attempting to detect {target}")
        return True  # Simplified; would check actual detection result

def main(args=None):
    rclpy.init(args=args)
    node = CognitivePlanningActionServer()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
```

## Error Handling and Plan Adaptation

### Adaptive Planning with Error Recovery

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import openai
import json
from enum import Enum

class PlanStatus(Enum):
    PENDING = "pending"
    EXECUTING = "executing"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    RECOVERING = "recovering"

class AdaptiveCognitivePlanner(Node):
    def __init__(self):
        super().__init__('adaptive_cognitive_planner')
        
        # Initialize OpenAI API
        openai.api_key = "your-api-key-here"
        self.model_name = "gpt-4"
        
        # Subscribers and publishers
        self.command_sub = self.create_subscription(
            String,
            '/adaptive_command',
            self.command_callback,
            10
        )
        
        self.execution_status_sub = self.create_subscription(
            String,
            '/execution_status',
            self.execution_status_callback,
            10
        )
        
        self.action_pub = self.create_publisher(
            String,
            '/adaptive_actions',
            10
        )
        
        self.get_logger().info("Adaptive Cognitive Planner initialized")
        
        # Track current plan and execution state
        self.current_plan = None
        self.plan_status = PlanStatus.PENDING
        self.current_step = 0
        self.recovery_attempts = 0
        self.max_recovery_attempts = 3

    def command_callback(self, msg):
        """Start a new plan based on command"""
        try:
            command = msg.data
            self.get_logger().info(f"Received new command: {command}")
            
            # Generate plan
            self.current_plan = self.generate_plan_with_error_handling(command)
            
            if self.current_plan:
                self.plan_status = PlanStatus.EXECUTING
                self.current_step = 0
                self.recovery_attempts = 0
                
                self.publish_next_action()
            else:
                self.get_logger().error("Failed to generate plan")
                
        except Exception as e:
            self.get_logger().error(f"Error in command callback: {e}")

    def execution_status_callback(self, msg):
        """Handle execution status updates"""
        try:
            status_data = json.loads(msg.data)
            status = status_data.get('status')
            error = status_data.get('error', '')
            
            if status == 'success':
                self.handle_step_success()
            elif status == 'failure':
                self.handle_step_failure(error)
            elif status == 'recovery_success':
                self.handle_recovery_success()
            elif status == 'recovery_failure':
                self.handle_recovery_failure()
                
        except Exception as e:
            self.get_logger().error(f"Error processing execution status: {e}")

    def handle_step_success(self):
        """Handle successful completion of a step"""
        self.current_step += 1
        
        if self.current_step >= len(self.current_plan.get('steps', [])):
            # Plan completed
            self.plan_status = PlanStatus.SUCCEEDED
            self.get_logger().info("Plan completed successfully")
        else:
            # Continue with next step
            self.publish_next_action()

    def handle_step_failure(self, error):
        """Handle failure of a step and attempt recovery"""
        self.get_logger().warn(f"Step failed with error: {error}")
        
        if self.recovery_attempts < self.max_recovery_attempts:
            self.plan_status = PlanStatus.RECOVERING
            self.recovery_attempts += 1
            
            # Ask LLM for recovery plan
            recovery_plan = self.generate_recovery_plan(error)
            
            if recovery_plan:
                self.execute_recovery_plan(recovery_plan)
            else:
                self.handle_recovery_failure()
        else:
            self.plan_status = PlanStatus.FAILED
            self.get_logger().error("Max recovery attempts reached, plan failed")

    def generate_recovery_plan(self, error):
        """Generate a recovery plan using the LLM"""
        system_prompt = f"""
        You are a helpful assistant for robotic error recovery. 
        A robot executing a plan has encountered the following error:
        
        Error: {error}
        
        Current plan state:
        - Current step: {self.current_step}
        - Plan: {self.current_plan}
        
        Generate a recovery plan to address this error. The recovery may involve:
        - Retrying the failed action
        - Trying an alternative approach
        - Adjusting parameters
        - Skipping to the next step if appropriate
        
        Respond in JSON format:
        {{
          "recovery_action": "action_to_take",
          "parameters": {{}},
          "explanation": "why this approach will work"
        }}
        """
        
        try:
            response = openai.ChatCompletion.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": "Generate a recovery plan for the error."}
                ],
                temperature=0.2,
                max_tokens=500
            )
            
            response_text = response.choices[0].message['content'].strip()
            
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            
            return json.loads(response_text)
            
        except Exception as e:
            self.get_logger().error(f"Error generating recovery plan: {e}")
            return None

    def execute_recovery_plan(self, recovery_plan):
        """Execute the recovery plan"""
        recovery_msg = {
            'action': 'recovery',
            'plan': recovery_plan,
            'original_step': self.current_step
        }
        
        recovery_msg_str = String()
        recovery_msg_str.data = json.dumps(recovery_msg)
        self.action_pub.publish(recovery_msg_str)

    def handle_recovery_success(self):
        """Handle successful recovery"""
        self.plan_status = PlanStatus.EXECUTING
        self.get_logger().info("Recovery successful, resuming plan")
        
        # Resume original plan
        self.publish_next_action()

    def handle_recovery_failure(self):
        """Handle failure during recovery attempt"""
        if self.recovery_attempts < self.max_recovery_attempts:
            self.get_logger().info("Recovery failed, attempting again")
            # Retry recovery
            error_msg = f"Previous recovery attempt failed after {self.recovery_attempts} attempts"
            self.handle_step_failure(error_msg)
        else:
            self.plan_status = PlanStatus.FAILED
            self.get_logger().error("Recovery failed, plan terminated")

    def publish_next_action(self):
        """Publish the next action in the plan"""
        if (self.current_plan and 
            self.current_step < len(self.current_plan.get('steps', []))):
            
            step = self.current_plan['steps'][self.current_step]
            
            action_msg = {
                'plan_id': self.current_plan.get('plan_id', 'unknown'),
                'step_id': self.current_step,
                'action': step.get('action'),
                'parameters': step.get('parameters', {}),
                'description': step.get('description', ''),
                'plan_total_steps': len(self.current_plan.get('steps', []))
            }
            
            action_msg_str = String()
            action_msg_str.data = json.dumps(action_msg)
            self.action_pub.publish(action_msg_str)
            
            self.get_logger().info(f"Published action: {step.get('description', 'Unknown')}")
        else:
            self.get_logger().warn("No action to publish or plan is invalid")

    def generate_plan_with_error_handling(self, command):
        """Generate a plan with built-in error handling"""
        system_prompt = f"""
        You are a helpful assistant that creates detailed plans for humanoid robots.
        The robot operates in real-world environments where errors and unexpected 
        situations can occur. Create a plan that includes potential error scenarios
        and appropriate responses.
        
        User command: {command}
        
        Include in your plan:
        1. Main execution steps
        2. Potential failure points
        3. Recovery strategies
        4. Validation steps
        
        Respond in JSON format:
        {{
          "plan_id": "unique_id",
          "original_command": "{command}",
          "steps": [
            {{
              "id": "step_1",
              "action": "action_type",
              "parameters": {{}},
              "description": "what the robot should do",
              "potential_errors": ["error1", "error2"],
              "recovery_strategies": ["strategy1", "strategy2"]
            }}
          ]
        }}
        """
        
        try:
            response = openai.ChatCompletion.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Create a detailed plan for: {command}"}
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            response_text = response.choices[0].message['content'].strip()
            
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            
            return json.loads(response_text)
            
        except Exception as e:
            self.get_logger().error(f"Error generating plan: {e}")
            return None

def main(args=None):
    rclpy.init(args=args)
    node = AdaptiveCognitivePlanner()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
```

## Best Practices for LLM-Based Planning

### Recommendations for Reliable Cognitive Planning

1. **Prompt Engineering**: Craft clear, specific prompts that guide the LLM to produce structured, usable outputs

2. **Validation**: Implement validation checks to verify the LLM's outputs are executable and safe

3. **Context Limitations**: Be aware of the context window limitations of LLMs and design your system accordingly

4. **Error Handling**: Implement robust error handling for LLM calls, which may fail or return unexpected results

5. **Security**: Ensure that API keys and sensitive information are properly secured

6. **Cost Management**: Monitor and manage API usage to control costs, especially for production systems

7. **Latency**: Consider caching strategies for common commands to reduce latency

8. **Fallback Mechanisms**: Have fallback approaches when LLM-based planning fails

LLM-based cognitive planning enables robots to understand and execute complex, natural language commands by leveraging the advanced reasoning capabilities of large language models. By properly integrating these systems with ROS 2 and implementing appropriate error handling and adaptation strategies, robots can perform complex tasks in dynamic, real-world environments.