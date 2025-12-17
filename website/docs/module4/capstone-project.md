---
sidebar_position: 4
title: Capstone Project - The Autonomous Humanoid
---

# Capstone Project: The Autonomous Humanoid

## Overview

The Capstone Project represents the culmination of all modules covered in this Physical AI & Humanoid Robotics course. Students will implement a complete autonomous humanoid system that can receive voice commands, plan paths, navigate obstacles, identify objects using computer vision, and manipulate objects to complete tasks. This project integrates all the foundational concepts learned throughout the course.

## Project Requirements

### Core Capabilities
Your autonomous humanoid system must demonstrate the following capabilities:

1. **Voice Command Reception**: Use OpenAI Whisper to process natural language commands
2. **Cognitive Planning**: Use LLMs to translate high-level commands into executable action sequences
3. **Path Planning**: Navigate to specified locations while avoiding obstacles
4. **Object Detection**: Identify and locate specific objects in the environment
5. **Manipulation**: Grasp and manipulate objects to complete tasks
6. **Human Interaction**: Respond appropriately to user commands and queries

### Example Scenario
A successful implementation might respond to a command like: "Go to the kitchen, find the red cup, and bring it to me" by:
- Understanding the voice command
- Planning a path to the kitchen area
- Navigating to the kitchen while avoiding obstacles
- Detecting and identifying the red cup
- Grasping the cup
- Returning to the user and placing the cup nearby

## System Architecture

The autonomous humanoid system architecture includes:

```
[Voice Input] → [Whisper ASR] → [LLM Cognitive Planner] → [Action Executor] → [Robot]
                    ↓                ↓                       ↓              ↓
[Environment] → [Perception] → [World Model] → [Behavior Engine] → [Physical Robot]
```

### Component Integration

1. **Voice Processing Module**: Handles speech-to-text conversion
2. **Cognitive Planning Module**: Translates commands to action sequences
3. **Navigation Module**: Handles path planning and obstacle avoidance
4. **Perception Module**: Detects and identifies objects
5. **Manipulation Module**: Controls robot arms and grippers
6. **Integration Layer**: Coordinates all modules using ROS 2

## Implementation Steps

### Phase 1: System Design and Integration

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped
from sensor_msgs.msg import Image
from builtin_interfaces.msg import Duration
import openai
import whisper
import json

class AutonomousHumanoidNode(Node):
    def __init__(self):
        super().__init__('autonomous_humanoid_node')
        
        # Initialize AI models
        openai.api_key = "your-openai-key-here"
        self.whisper_model = whisper.load_model("base")
        
        # System state
        self.system_state = "idle"  # idle, listening, processing, executing
        self.current_task = None
        self.robot_pose = None
        self.detected_objects = {}
        
        # Create subscribers for all components
        self.voice_command_sub = self.create_subscription(
            String,
            '/voice_command',
            self.voice_command_callback,
            10
        )
        
        self.robot_pose_sub = self.create_subscription(
            PoseStamped,
            '/robot_pose',
            self.pose_callback,
            10
        )
        
        self.object_detection_sub = self.create_subscription(
            String,  # Simplified - in practice this would be a more complex message
            '/detected_objects',
            self.object_detection_callback,
            10
        )
        
        self.execution_status_sub = self.create_subscription(
            String,
            '/execution_status',
            self.execution_status_callback,
            10
        )
        
        # Create publishers
        self.action_pub = self.create_publisher(
            String,
            '/planned_actions',
            10
        )
        
        self.speech_pub = self.create_publisher(
            String,
            '/robot_speech',
            10
        )
        
        self.get_logger().info("Autonomous Humanoid Node initialized")
        
        # Timer for system monitoring
        self.timer = self.create_timer(1.0, self.system_monitor)

    def voice_command_callback(self, msg):
        """Process voice command and initiate task execution"""
        try:
            command = msg.data
            
            if self.system_state == "idle":
                self.system_state = "processing"
                self.get_logger().info(f"Received command: {command}")
                
                # Generate plan using LLM
                plan = self.generate_task_plan(command)
                
                if plan:
                    self.current_task = plan
                    self.get_logger().info(f"Generated plan: {plan}")
                    
                    # Publish first action
                    self.publish_action(plan['steps'][0] if plan['steps'] else None)
                    
                    # Announce task
                    self.speak(f"Starting task: {command}")
                else:
                    self.system_state = "idle"
                    self.speak("Sorry, I couldn't understand the command")
                    
        except Exception as e:
            self.get_logger().error(f"Error processing voice command: {e}")
            self.system_state = "idle"

    def generate_task_plan(self, command):
        """Generate a task plan using LLM"""
        system_prompt = f"""
        You are a helpful assistant for a humanoid robot. The user has given the command: "{command}"
        
        Generate a plan with the following JSON structure:
        {{
          "task": "{command}",
          "steps": [
            {{
              "id": 1,
              "action": "action_type",
              "description": "what to do",
              "parameters": {{"target": "object", "location": "coordinates"}}
            }}
          ]
        }}
        
        Action types: navigate_to, detect_object, pick_up, place, speak
        """
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Generate a plan for: {command}"}
                ],
                temperature=0.3,
                max_tokens=500
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

    def pose_callback(self, msg):
        """Update robot's current pose"""
        self.robot_pose = {
            'x': msg.pose.position.x,
            'y': msg.pose.position.y,
            'z': msg.pose.position.z
        }

    def object_detection_callback(self, msg):
        """Update detected objects"""
        try:
            objects = json.loads(msg.data)
            self.detected_objects = objects
        except Exception as e:
            self.get_logger().error(f"Error parsing object detection: {e}")

    def execution_status_callback(self, msg):
        """Handle execution status updates"""
        try:
            status = json.loads(msg.data)
            
            if status.get('status') == 'completed':
                # Move to next step in task
                if self.current_task:
                    current_step = status.get('step', 0)
                    next_step_idx = current_step + 1
                    
                    if next_step_idx < len(self.current_task['steps']):
                        # Execute next step
                        next_step = self.current_task['steps'][next_step_idx]
                        self.publish_action(next_step)
                    else:
                        # Task completed
                        self.get_logger().info("Task completed successfully")
                        self.speak("Task completed")
                        self.system_state = "idle"
                        self.current_task = None
            elif status.get('status') == 'failed':
                # Handle failure
                self.get_logger().error(f"Task step failed: {status.get('error')}")
                self.speak("Sorry, I encountered an error")
                self.system_state = "idle"
                self.current_task = None
                
        except Exception as e:
            self.get_logger().error(f"Error processing execution status: {e}")

    def publish_action(self, action):
        """Publish action for execution"""
        if action:
            action_msg = String()
            action_msg.data = json.dumps(action)
            self.action_pub.publish(action_msg)
            
            self.get_logger().info(f"Published action: {action}")

    def speak(self, text):
        """Make the robot speak"""
        speech_msg = String()
        speech_msg.data = text
        self.speech_pub.publish(speech_msg)

    def system_monitor(self):
        """Monitor system state and report"""
        self.get_logger().info(f"System state: {self.system_state}")

def main(args=None):
    rclpy.init(args=args)
    node = AutonomousHumanoidNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
```

### Phase 2: Voice Command Processing Integration

Create a voice command processing node that integrates Whisper with the system:

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Bool
from sensor_msgs.msg import AudioData
import whisper
import pyaudio
import wave
import tempfile
import os
import threading
import queue

class VoiceCommandProcessor(Node):
    def __init__(self):
        super().__init__('voice_command_processor')
        
        # Initialize Whisper model
        self.model = whisper.load_model("base")
        
        # Audio parameters
        self.rate = 16000
        self.chunk = 1024
        self.channels = 1
        self.record_seconds = 3
        
        # Publishers and subscribers
        self.command_pub = self.create_publisher(
            String,
            '/voice_command',
            10
        )
        
        self.listening_pub = self.create_publisher(
            Bool,
            '/is_listening',
            10
        )
        
        # Audio processing
        self.audio_queue = queue.Queue()
        self.is_listening = False
        
        # Start audio recording thread
        self.audio_thread = threading.Thread(target=self.record_audio)
        self.audio_thread.daemon = True
        self.audio_thread.start()
        
        self.get_logger().info("Voice Command Processor initialized")

    def start_listening(self):
        """Start listening for voice commands"""
        self.is_listening = True
        self.get_logger().info("Started listening for voice commands")

    def stop_listening(self):
        """Stop listening for voice commands"""
        self.is_listening = False
        self.get_logger().info("Stopped listening for voice commands")

    def record_audio(self):
        """Continuously record audio when listening is enabled"""
        import pyaudio
        
        audio = pyaudio.PyAudio()
        
        while True:  # Keep running
            if not self.is_listening:
                # Send status update
                status_msg = Bool()
                status_msg.data = False
                self.listening_pub.publish(status_msg)
                
                # Wait before checking again
                import time
                time.sleep(0.1)
                continue
            
            # Send status update
            status_msg = Bool()
            status_msg.data = True
            self.listening_pub.publish(status_msg)
            
            # Record a chunk of audio
            stream = audio.open(
                format=pyaudio.paInt16,
                channels=self.channels,
                rate=self.rate,
                input=True,
                frames_per_buffer=self.chunk
            )
            
            frames = []
            for _ in range(0, int(self.rate / self.chunk * self.record_seconds)):
                data = stream.read(self.chunk)
                frames.append(data)
            
            stream.stop_stream()
            stream.close()
            
            # Process audio
            self.process_audio_chunk(frames)
            
            # Small delay to prevent excessive processing
            import time
            time.sleep(0.1)

    def process_audio_chunk(self, frames):
        """Process a chunk of audio with Whisper"""
        try:
            # Create WAV data from frames
            import struct
            
            # WAV header
            wav_header = self.create_wav_header(len(b''.join(frames)), self.rate, self.channels, 16)
            wav_data = wav_header + b''.join(frames)
            
            # Write to temporary file
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                temp_file.write(wav_data)
                temp_file_path = temp_file.name
            
            # Transcribe
            result = self.model.transcribe(temp_file_path)
            text = result['text'].strip()
            
            # Clean up
            os.unlink(temp_file_path)
            
            # Only publish non-empty text
            if text:
                # Check if it's a command (not just random noise)
                if self.is_command(text):
                    self.get_logger().info(f"Recognized command: {text}")
                    
                    command_msg = String()
                    command_msg.data = text
                    self.command_pub.publish(command_msg)
                else:
                    self.get_logger().info(f"Ignored: {text} (doesn't appear to be a command)")
                    
        except Exception as e:
            self.get_logger().error(f"Error processing audio chunk: {e}")

    def create_wav_header(self, data_size, sample_rate, channels, bits_per_sample):
        """Create WAV file header"""
        import struct
        
        byte_rate = sample_rate * channels * bits_per_sample // 8
        block_align = channels * bits_per_sample // 8
        
        header = b'RIFF'
        header += struct.pack('<I', data_size + 36)
        header += b'WAVE'
        header += b'fmt '
        header += struct.pack('<I', 16)
        header += struct.pack('<H', 1)   # Audio format (1 = PCM)
        header += struct.pack('<H', channels)
        header += struct.pack('<I', sample_rate)
        header += struct.pack('<I', byte_rate)
        header += struct.pack('<H', block_align)
        header += struct.pack('<H', bits_per_sample)
        header += b'data'
        header += struct.pack('<I', data_size)
        
        return header

    def is_command(self, text):
        """Determine if recognized text is likely a command"""
        # Look for keywords that indicate commands
        command_keywords = [
            'go', 'move', 'walk', 'turn', 'stop', 'start', 'begin',
            'pick', 'grab', 'take', 'place', 'put', 'drop',
            'find', 'locate', 'search', 'look', 'see',
            'open', 'close', 'turn on', 'turn off',
            'bring', 'get', 'fetch', 'come', 'follow', 'help'
        ]
        
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in command_keywords)

def main(args=None):
    rclpy.init(args=args)
    node = VoiceCommandProcessor()
    
    try:
        # Start listening
        node.start_listening()
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.stop_listening()
        node.destroy_node()
        rclpy.shutdown()
```

### Phase 3: Object Detection Integration

Create an object detection node that identifies objects for manipulation:

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String
from geometry_msgs.msg import Point
from cv_bridge import CvBridge
import cv2
import numpy as np
import json

class ObjectDetectionNode(Node):
    def __init__(self):
        super().__init__('object_detection_node')
        
        # Initialize OpenCV bridge
        self.bridge = CvBridge()
        
        # Subscribe to camera feed
        self.image_sub = self.create_subscription(
            Image,
            '/camera/rgb/image_raw',
            self.image_callback,
            10
        )
        
        # Publish detected objects
        self.object_pub = self.create_publisher(
            String,
            '/detected_objects',
            10
        )
        
        self.get_logger().info("Object Detection Node initialized")

    def image_callback(self, msg):
        """Process incoming image and detect objects"""
        try:
            # Convert ROS Image message to OpenCV
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
            
            # Perform object detection
            detected_objects = self.detect_objects(cv_image)
            
            # Publish results
            if detected_objects:
                objects_msg = String()
                objects_msg.data = json.dumps(detected_objects)
                self.object_pub.publish(objects_msg)
                
                self.get_logger().info(f"Detected objects: {list(detected_objects.keys())}")
                
        except Exception as e:
            self.get_logger().error(f"Error processing image: {e}")

    def detect_objects(self, image):
        """Detect objects in the image"""
        # For this example, we'll use color-based detection
        # In practice, you'd use a more sophisticated model like YOLO or Detectron2
        
        detected_objects = {}
        
        # Convert to HSV for better color detection
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Define color ranges for different objects
        color_ranges = {
            'red': ([0, 50, 50], [10, 255, 255]),
            'blue': ([100, 50, 50], [130, 255, 255]),
            'green': ([40, 50, 50], [80, 255, 255]),
            'yellow': ([20, 50, 50], [40, 255, 255])
        }
        
        height, width = image.shape[:2]
        
        for color_name, (lower, upper) in color_ranges.items():
            # Create mask for this color
            mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
            
            # Find contours
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Process each contour
            for i, contour in enumerate(contours):
                area = cv2.contourArea(contour)
                
                # Only consider contours with significant area
                if area > 500:  # Adjust threshold as needed
                    # Calculate centroid
                    M = cv2.moments(contour)
                    if M["m00"] != 0:
                        cX = int(M["m10"] / M["m00"])
                        cY = int(M["m01"] / M["m00"])
                        
                        # Convert to normalized coordinates (0-1)
                        norm_x = cX / width
                        norm_y = cY / height
                        
                        # Calculate bounding box
                        x, y, w, h = cv2.boundingRect(contour)
                        
                        # Store object information
                        object_id = f"{color_name}_{i}"
                        detected_objects[object_id] = {
                            'name': color_name,
                            'color': color_name,
                            'centroid': {'x': float(norm_x), 'y': float(norm_y)},
                            'bbox': {'x': float(x)/width, 'y': float(y)/height, 
                                   'width': float(w)/width, 'height': float(h)/height},
                            'area': float(area) / (width * height),
                            'confidence': min(1.0, area / 10000)  # Normalize confidence
                        }
        
        return detected_objects

def main(args=None):
    rclpy.init(args=args)
    node = ObjectDetectionNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
```

### Phase 4: Navigation and Path Planning

Create a navigation node that handles path planning and obstacle avoidance:

```python
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped, Twist
from nav_msgs.msg import Path, Odometry
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String, Bool
import numpy as np
import json

class NavigationNode(Node):
    def __init__(self):
        super().__init__('navigation_node')
        
        # Subscribers
        self.goal_sub = self.create_subscription(
            PoseStamped,
            '/navigation_goal',
            self.goal_callback,
            10
        )
        
        self.odom_sub = self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            10
        )
        
        self.scan_sub = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10
        )
        
        # Publishers
        self.cmd_vel_pub = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )
        
        self.status_pub = self.create_publisher(
            String,
            '/navigation_status',
            10
        )
        
        # Navigation parameters
        self.linear_speed = 0.3  # m/s
        self.angular_speed = 0.5  # rad/s
        self.goal_tolerance = 0.2  # meters
        self.obstacle_threshold = 0.5  # meters
        
        # State variables
        self.current_pose = None
        self.current_goal = None
        self.velocity = Twist()
        self.scan_data = None
        self.navigating = False
        
        # Timer for navigation control
        self.nav_timer = self.create_timer(0.1, self.navigation_control)
        
        self.get_logger().info("Navigation Node initialized")

    def goal_callback(self, msg):
        """Set new navigation goal"""
        self.current_goal = msg.pose
        self.navigating = True
        self.get_logger().info(f"New goal set: ({msg.pose.position.x}, {msg.pose.position.y})")

    def odom_callback(self, msg):
        """Update current pose from odometry"""
        self.current_pose = msg.pose.pose

    def scan_callback(self, msg):
        """Update laser scan data"""
        self.scan_data = np.array(msg.ranges)

    def navigation_control(self):
        """Main navigation control loop"""
        if not self.navigating or self.current_goal is None or self.current_pose is None:
            # Stop if not navigating
            if self.velocity.linear.x != 0 or self.velocity.angular.z != 0:
                self.velocity.linear.x = 0.0
                self.velocity.angular.z = 0.0
                self.cmd_vel_pub.publish(self.velocity)
            return

        # Check for obstacles
        if self.scan_data is not None:
            min_distance = np.min(self.scan_data[np.isfinite(self.scan_data)])
            
            if min_distance < self.obstacle_threshold:
                # Stop if obstacle is too close
                self.velocity.linear.x = 0.0
                self.velocity.angular.z = 0.0
                self.cmd_vel_pub.publish(self.velocity)
                
                status_msg = String()
                status_msg.data = json.dumps({
                    'status': 'obstacle_detected',
                    'distance': float(min_distance)
                })
                self.status_pub.publish(status_msg)
                return

        # Calculate direction to goal
        dx = self.current_goal.position.x - self.current_pose.position.x
        dy = self.current_goal.position.y - self.current_pose.position.y
        distance_to_goal = np.sqrt(dx*dx + dy*dy)

        if distance_to_goal < self.goal_tolerance:
            # Reached goal
            self.velocity.linear.x = 0.0
            self.velocity.angular.z = 0.0
            self.cmd_vel_pub.publish(self.velocity)
            self.navigating = False
            
            status_msg = String()
            status_msg.data = json.dumps({
                'status': 'goal_reached',
                'distance': float(distance_to_goal)
            })
            self.status_pub.publish(status_msg)
            return

        # Calculate desired orientation
        desired_yaw = np.arctan2(dy, dx)
        
        # Get current orientation
        current_yaw = self.get_yaw_from_quaternion(self.current_pose.orientation)
        
        # Calculate orientation error
        angle_error = desired_yaw - current_yaw
        
        # Normalize angle error to [-π, π]
        while angle_error > np.pi:
            angle_error -= 2 * np.pi
        while angle_error < -np.pi:
            angle_error += 2 * np.pi

        # Control logic
        if abs(angle_error) > 0.1:  # If not facing the right direction
            self.velocity.linear.x = 0.0
            self.velocity.angular.z = np.clip(angle_error * 1.0, -self.angular_speed, self.angular_speed)
        else:
            # Move forward
            self.velocity.linear.x = min(self.linear_speed, distance_to_goal * 1.0)  # Proportional to distance
            self.velocity.angular.z = 0.0

        # Publish velocity command
        self.cmd_vel_pub.publish(self.velocity)

        # Publish status
        status_msg = String()
        status_msg.data = json.dumps({
            'status': 'navigating',
            'distance_to_goal': float(distance_to_goal),
            'angle_error': float(angle_error),
            'linear_velocity': float(self.velocity.linear.x),
            'angular_velocity': float(self.velocity.angular.z)
        })
        self.status_pub.publish(status_msg)

    def get_yaw_from_quaternion(self, orientation):
        """Extract yaw angle from quaternion"""
        import math
        siny_cosp = 2 * (orientation.w * orientation.z + orientation.x * orientation.y)
        cosy_cosp = 1 - 2 * (orientation.y * orientation.y + orientation.z * orientation.z)
        yaw = math.atan2(siny_cosp, cosy_cosp)
        return yaw

def main(args=None):
    rclpy.init(args=args)
    node = NavigationNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
```

## Testing and Evaluation

### Testing Scenarios

Your autonomous humanoid system should be tested with various scenarios:

1. **Simple Navigation**: "Go to the kitchen"
2. **Object Interaction**: "Bring me the red cup"
3. **Complex Tasks**: "Go to the kitchen, find the blue bottle, and place it on the table"
4. **Error Recovery**: Testing how the system handles unexpected situations

### Performance Metrics

Evaluate your system based on:
- **Success Rate**: Percentage of tasks completed successfully
- **Response Time**: Time from command to task initiation
- **Task Completion Time**: Time to complete the requested task
- **Accuracy**: How accurately objects are detected and manipulated
- **Robustness**: How well the system handles errors and unexpected situations

## Deployment Considerations

### Simulation vs. Real World

Your system should be developed and tested in simulation first using tools from Modules 1-3, then deployed to a physical robot. Considerations for real-world deployment include:

1. **Sensor Noise**: Real sensors have more noise than simulated ones
2. **Timing Differences**: Real robots have different response times
3. **Environmental Variability**: Real environments change and are less predictable
4. **Safety Requirements**: Physical safety measures must be in place

### Hardware Requirements

For the complete system, ensure your hardware meets the requirements from the course hardware section, particularly:
- Sufficient GPU power for real-time perception and AI processing
- Adequate CPU power for control systems
- Proper sensors (camera, LiDAR, IMU)
- Actuators for manipulation tasks

## Conclusion

The Autonomous Humanoid capstone project integrates all aspects of Physical AI and humanoid robotics covered in this course. It demonstrates how to combine perception, planning, control, and AI to create an intelligent system capable of understanding natural language commands and executing complex tasks in physical environments.

This project represents the state-of-the-art in embodied AI and provides a foundation for advanced research and development in humanoid robotics. Successfully implementing this system requires mastery of all modules covered in the course, making it an excellent demonstration of your knowledge and skills in Physical AI.