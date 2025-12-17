---
sidebar_position: 2
title: ROS 2 Nodes, Topics, and Services
---

# ROS 2 Nodes, Topics, and Services

## Understanding the ROS 2 Communication Model

ROS 2 implements a distributed computing framework where different functionalities are encapsulated in separate processes called **nodes**. These nodes communicate with each other through a publish-subscribe model using **topics**, request-response patterns with **services**, and action-based communication for long-running tasks.

## Nodes: The Building Blocks of ROS 2

A ROS 2 node is an executable that uses ROS 2 client library to communicate with other nodes. Nodes are designed to perform a specific task, such as:

- Controlling a sensor or actuator
- Processing sensory data
- Implementing a control algorithm
- Providing a user interface

### Creating a ROS 2 Node in Python

```python
import rclpy
from rclpy.node import Node

class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello World: %d' % self.i
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1

def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = MinimalPublisher()
    rclpy.spin(minimal_publisher)
    minimal_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Topics: The Publish-Subscribe Pattern

Topics in ROS 2 implement a one-to-many publisher-subscriber communication model. Publishers send data to a topic and any number of subscribers can receive that data. This decouples publishers from subscribers, allowing for flexible system design.

### Characteristics of Topics:
- **Asynchronous**: Publishers send messages without waiting for a response
- **Broadcast**: One publisher can send to multiple subscribers
- **Message queues**: Allow for buffering when publishers and subscribers run at different rates
- **Type safety**: All messages on a topic must be of the same message type

### Example: Publisher and Subscriber Pair

**Publisher:**
```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class Talker(Node):
    def __init__(self):
        super().__init__('talker')
        self.publisher = self.create_publisher(String, 'chatter', 10)
        timer_period = 0.5
        self.timer = self.create_timer(timer_period, self.timer_callback)
    
    def timer_callback(self):
        msg = String()
        msg.data = 'Hello World'
        self.publisher.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    talker = Talker()
    rclpy.spin(talker)
    talker.destroy_node()
    rclpy.shutdown()
```

**Subscriber:**
```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class Listener(Node):
    def __init__(self):
        super().__init__('listener')
        self.subscription = self.create_subscription(
            String,
            'chatter',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)

def main(args=None):
    rclpy.init(args=args)
    listener = Listener()
    rclpy.spin(listener)
    listener.destroy_node()
    rclpy.shutdown()
```

## Services: Request-Response Communication

Services implement a synchronous request-response pattern where a client sends a request to a service and waits for a response. This is useful for operations that have a clear beginning and end.

### Characteristics of Services:
- **Synchronous**: Client waits for a response
- **One-to-one**: One client requests from one service
- **Request-Response**: Each request gets exactly one response
- **Well-defined interfaces**: Both request and response message types are specified

### Example: Service Server and Client

**Service Server:**
```python
from example_interfaces.srv import AddTwoInts
import rclpy
from rclpy.node import Node

class MinimalService(Node):

    def __init__(self):
        super().__init__('minimal_service')
        self.srv = self.create_service(AddTwoInts, 'add_two_ints', self.add_two_ints_callback)

    def add_two_ints_callback(self, request, response):
        response.sum = request.a + request.b
        self.get_logger().info('Incoming request\na: %d b: %d' % (request.a, request.b))
        return response

def main(args=None):
    rclpy.init(args=args)
    minimal_service = MinimalService()
    rclpy.spin(minimal_service)
    rclpy.shutdown()
```

**Service Client:**
```python
import sys
from example_interfaces.srv import AddTwoInts
import rclpy
from rclpy.node import Node

class MinimalClientAsync(Node):

    def __init__(self):
        super().__init__('minimal_client_async')
        self.cli = self.create_client(AddTwoInts, 'add_two_ints')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = AddTwoInts.Request()

    def send_request(self, a, b):
        self.req.a = a
        self.req.b = b
        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()

def main(args=None):
    rclpy.init(args=args)
    minimal_client = MinimalClientAsync()
    response = minimal_client.send_request(int(sys.argv[1]), int(sys.argv[2]))
    minimal_client.get_logger().info(
        'Result of add_two_ints: for %d + %d = %d' % 
        (int(sys.argv[1]), int(sys.argv[2]), response.sum))
    minimal_client.destroy_node()
    rclpy.shutdown()
```

## Practical Considerations for Humanoid Robots

Humanoid robots typically involve complex communication patterns:

- **Sensor nodes** publish data like joint angles, IMU readings, and camera feeds to topics
- **Perception nodes** subscribe to sensor data and publish processed information like object locations
- **Planning nodes** might provide services to compute paths or trajectories
- **Control nodes** subscribe to commands and control the physical robot
- **Behavior nodes** coordinate between different subsystems using a combination of topics and services

## Best Practices

1. **Node Granularity**: Create nodes that perform well-defined functions rather than trying to do too much in one node
2. **Topic Naming**: Use descriptive names that indicate the data being published
3. **Message Types**: Use existing message types when possible, or define custom messages that meet your needs
4. **Quality of Service**: Understand QoS settings for different types of communication
5. **Error Handling**: Implement proper error handling in your nodes
6. **Logging**: Use appropriate logging levels to aid in debugging

Understanding these fundamental ROS 2 concepts is crucial for developing complex robotic systems. In the next section, we'll explore how to bridge Python-based AI agents with ROS 2 controllers using rclpy.