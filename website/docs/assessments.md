---
sidebar_position: 5
title: Assessments
---

# Assessments

The assessment strategy for the Physical AI & Humanoid Robotics course combines practical project work with theoretical understanding. Each assessment is designed to evaluate both technical competency and practical application of embodied intelligence concepts.

## Module-Specific Projects

### ROS 2 Package Development Project
- **Objective**: Develop a complete ROS 2 package that implements a specific robotic functionality
- **Requirements**:
  - Design and implement at least 3 interconnected nodes
  - Integrate sensors and actuators with proper message passing
  - Create launch files for complete system initialization
  - Document the package with comments and README
- **Evaluation Criteria**:
  - Code quality and architecture (30%)
  - Functionality and robustness (40%)
  - Documentation and maintainability (20%)
  - Innovation and problem-solving (10%)

### Gazebo Simulation Implementation
- **Objective**: Create a realistic simulation environment with a robot performing a specific task
- **Requirements**:
  - Design a 3D environment with relevant obstacles and objects
  - Implement physics-based interactions
  - Simulate multiple sensor types (LiDAR, cameras, IMUs)
  - Demonstrate the robot completing a navigation or manipulation task
- **Evaluation Criteria**:
  - Simulation realism and physics accuracy (35%)
  - Sensor simulation fidelity (25%)
  - Task completion and robot behavior (25%)
  - Optimization and performance (15%)

### Isaac-Based Perception Pipeline
- **Objective**: Build a perception system using NVIDIA Isaac tools
- **Requirements**:
  - Implement a VSLAM (Visual SLAM) system
  - Integrate computer vision for object detection/reognition
  - Demonstrate performance in both simulation and real-world data
  - Optimize for edge deployment constraints
- **Evaluation Criteria**:
  - Perceptual accuracy and reliability (40%)
  - Computational efficiency (25%)
  - Robustness across different environments (20%)
  - Integration with navigation stack (15%)

## Capstone Project: Simulated Humanoid Robot with Conversational AI

### Project Overview
The capstone project integrates all concepts learned throughout the quarter by developing a simulated humanoid robot capable of receiving voice commands, planning paths, navigating obstacles, identifying objects using computer vision, and manipulating them.

### Requirements
- **Voice Command Processing**: Integrate OpenAI Whisper for speech recognition
- **Cognitive Planning**: Use LLMs to translate natural language commands into sequences of ROS 2 actions
- **Navigation System**: Implement Nav2-based path planning for bipedal humanoid movement
- **Computer Vision**: Identify and locate objects in the environment
- **Manipulation**: Execute appropriate manipulation actions for identified objects
- **Human Interaction**: Demonstrate natural language interface for robot interaction

### Evaluation Criteria
- **Integration Quality** (25%): How well all components work together
- **Task Completion** (25%): Successful execution of the complete task sequence
- **Innovation** (20%): Creative solutions to challenges encountered
- **Technical Soundness** (15%): Proper implementation of underlying technologies
- **Presentation** (15%): Clear demonstration and documentation of the project

## Practical Assignments

### Assignment 1: URDF Humanoid Modeling
- Create a complete URDF model of a humanoid robot
- Include all necessary joints and links for bipedal locomotion
- Add visual and collision geometries
- Validate the model in both Gazebo and RViz

### Assignment 2: Sim-to-Real Transfer
- Develop a control algorithm in simulation
- Document the process of adapting the algorithm for real-world deployment
- Analyze and address the sim-to-real gap
- Demonstrate performance comparison

### Assignment 3: Conversational Robotics Interface
- Design a natural language interface for a specific robotic task
- Implement speech recognition and response generation
- Ensure the system handles ambiguous or incorrect inputs gracefully
- Evaluate the interface with human users

## Examinations

### Midterm Examination
- Covers Weeks 1-7 (Physical AI foundations through simulation)
- Format: 50% conceptual understanding, 50% practical problem-solving
- Focus on understanding the theoretical foundations of embodied intelligence and simulation techniques

### Final Examination
- Covers Weeks 8-13 (Isaac platform through conversational robotics)
- Format: 40% conceptual understanding, 60% design challenges
- Focus on integrating multiple technologies and solving complex robotics problems

## Continuous Assessment

### Class Participation and Labs (10%)
- Active participation in laboratory sessions
- Peer collaboration and code review
- Problem-solving contribution during practical sessions

### Peer Review Process (5%)
- Review and provide constructive feedback on fellow students' projects
- Participate in code and design reviews
- Demonstrate understanding through critical analysis

## Rubric for Project Evaluation

### Excellent (A: 90-100%)
- Demonstrates exceptional understanding of concepts
- Implements innovative solutions to complex problems
- Code is well-structured, documented, and maintainable
- Systems are robust and reliable in diverse conditions
- Presentation clearly articulates design decisions and outcomes

### Good (B: 80-89%)
- Shows solid understanding of concepts
- Successfully implements required functionality
- Code is organized and reasonably well documented
- Systems work reliably under normal conditions
- Presentation covers key aspects of the implementation

### Satisfactory (C: 70-79%)
- Demonstrates basic understanding of concepts
- Implements required functionality with some limitations
- Code has basic structure and documentation
- Systems work under specific conditions
- Presentation covers essential aspects

### Needs Improvement (D: 60-69%)
- Shows limited understanding of concepts
- Implementation has significant limitations
- Code lacks organization or documentation
- Systems have reliability issues
- Presentation lacks depth or clarity

### Unsatisfactory (F: Below 60%)
- Demonstrates poor understanding of concepts
- Implementation fails to meet basic requirements
- Code is disorganized or unclear
- Systems are unreliable
- Presentation is inadequate

## Special Considerations

### Late Submission Policy
- Assignments submitted late will be penalized 5% per day
- Capstone project has a hard deadline with no late submissions accepted
- Extensions may be granted for documented emergencies

### Collaboration Policy
- Individual assignments must be completed independently
- Group projects require clear documentation of individual contributions
- Code sharing is permitted only within project teams
- All sources must be properly cited

### Accommodation Policy
- Students requiring accommodations should contact the appropriate services early in the quarter
- Alternative assessment formats are available when needed
- Extended time may be provided for documented needs