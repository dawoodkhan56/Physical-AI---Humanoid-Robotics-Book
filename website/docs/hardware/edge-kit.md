---
sidebar_position: 3
title: The Physical AI Edge Kit
---

# The Physical AI Edge Kit

## Overview

Since full humanoid robots are expensive, students learn "Physical AI" by setting up the nervous system on a desk before deploying to a robot. This Edge Kit covers Module 3 (Isaac ROS) and Module 4 (VLA) by allowing you to deploy your ROS 2 nodes and understand resource constraints compared to your powerful workstations.

## The Brain: NVIDIA Jetson Platform

### Recommended Options
- **NVIDIA Jetson Orin Nano (8GB)** or **Orin NX (16GB)**

### Why the Jetson Platform
- Industry standard for embodied AI
- Students deploy ROS 2 nodes here to understand resource constraints
- Supports Isaac ROS packages for accelerated perception
- Power efficient for embedded applications

### Jetson Platform Comparison

| Model | RAM | Performance | Price | Best For |
|-------|-----|-------------|-------|----------|
| Jetson Orin Nano | 8GB | Good | ~$400-500 | Budget-conscious learning |
| Jetson Orin NX | 16GB | Better | ~$600-700 | More demanding applications |

### Key Features
- 10W-25W power consumption depending on model
- ARM-based processor optimized for AI workloads
- Integrated GPU for accelerated inference
- Multiple camera interfaces
- GPIO pins for hardware control

## The Eyes: Vision Sensors

### Recommended: Intel RealSense D435i or D455
- Provides RGB (Color) and Depth (Distance) data
- Essential for the VSLAM and Perception modules
- Built-in IMU for enhanced sensor fusion

### RealSense Model Comparison

| Model | Features | Price | Best Use |
|-------|----------|-------|----------|
| D435i | RGB, Depth, IMU | ~$350 | Primary choice for course |
| D455 | RGB, Depth, IMU, higher resolution | ~$500 | Higher precision applications |

### Why RealSense?
- Well-supported ROS packages
- Accurate depth sensing
- Good integration with Gazebo simulation
- Provides both visual and depth information critical for perception

## The Inner Ear: Balance and Orientation

### IMU (Inertial Measurement Unit)
- Generic USB IMU (BNO055) 
- Often built into the RealSense D435i or Jetson boards
- A separate module helps teach IMU calibration concepts

### Why IMU Matters
- Critical for balance control in humanoid robots
- Provides orientation and motion data
- Essential for SLAM algorithms
- Helps understand sensor fusion

## Voice Interface

### Recommended: ReSpeaker USB Mic Array v2.0
- Far-field microphone for voice commands (Module 4)
- Multiple microphones for sound localization
- USB interface for easy integration

### Alternative Voice Interfaces
- USB headset with microphone
- Webcam with built-in microphone (lower quality)
- Smartphone audio input (for testing only)

## Additional Components

### Power and Connectivity
- **Power Supply**: Appropriate voltage/current for Jetson board
- **High-endurance microSD card (128GB)**: For the OS and applications
- **Jumper wires and basic electronics components**: For hardware connections
- **USB Hub**: If additional peripherals needed
- **Ethernet cable**: For reliable network connection during development

### Optional Enhancements
- **LiDAR sensor** (e.g., RPLIDAR A1): For additional mapping capabilities
- **Additional cameras**: For stereo vision experiments
- **Robot manipulator arm**: For early manipulation experiments

## Total Kit Cost

| Component | Model | Price (Approx.) | Notes |
|-----------|-------|-----------------|-------|
| The Brain | NVIDIA Jetson Orin Nano Super Dev Kit (8GB) | $249 | New official MSRP (Price dropped from ~$499). Capable of 40 TOPS. |
| The Eyes | Intel RealSense D435i | $349 | Includes IMU (essential for SLAM). Do not buy the D435 (non-i). |
| The Ears | ReSpeaker USB Mic Array v2.0 | $69 | Far-field microphone for voice commands (Module 4). |
| Wi-Fi | (Included in Dev Kit) | $0 | The new "Super" kit includes the Wi-Fi module pre-installed. |
| Power/Misc | SD Card (128GB) + Jumper Wires | $30 | High-endurance microSD card required for the OS. |

**TOTAL: ~$700 per kit**

## Educational Value of the Edge Kit

### Understanding Resource Constraints
- Limited computational power compared to workstations
- Memory constraints requiring efficient algorithms
- Power consumption considerations
- Real-world deployment constraints

### Practical Skills Developed
- Optimizing AI models for embedded deployment
- Real-time processing requirements
- Hardware-software integration
- Sensor fusion techniques
- Debugging on embedded platforms

## Alternative: Cloud-Based Development

For students unable to acquire the Edge Kit immediately, consider:
- NVIDIA Isaac ROS Docker containers for development
- Simulation-only development initially
- Cloud-based Jetson development environments
- Later acquisition of hardware for deployment

The Edge Kit provides the practical experience necessary to understand the challenges of deploying AI systems to physical robots, making it a valuable investment for serious students of Physical AI.