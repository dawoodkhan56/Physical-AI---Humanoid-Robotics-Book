---
sidebar_position: 4
title: The Robot Lab
---

# The Robot Lab

## Overview

For the "Physical" part of the course, you have three tiers of options depending on budget and objectives. All options should allow students to apply the software principles learned in Modules 1-4 (ROS 2, VSLAM, Isaac Sim) effectively.

## Option A: The "Proxy" Approach (Recommended for Budget-Conscious Programs)

### Hardware: Unitree Go2 Edu
- **Price**: ~$1,800 - $3,000
- **Pros**: 
  - Highly durable, suitable for student use
  - Excellent ROS 2 support
  - Affordable enough to have multiple units
  - Good for learning basic locomotion and control
- **Cons**: 
  - Not a biped (humanoid), so some concepts don't transfer directly
  - More complex than single-arm systems

### Why Go2 Edu Works Well:
- Robust enough for student experimentation
- Good documentation and community support
- Appropriate complexity for learning robotics concepts
- Can implement many of the same software stacks as humanoids

## Option B: The "Miniature Humanoid" Approach

### Hardware Options:

#### Unitree G1 (~$16k)
- More affordable than full-size humanoids
- One of the few commercially available humanoids that can walk dynamically
- Has an SDK open enough for students to inject their own ROS 2 controllers
- More realistic representation of humanoid challenges

#### Robotis OP3 (~$12k, older but stable)
- Proven platform with educational focus
- Good documentation and educational materials
- Supports more advanced research

#### Budget Alternative: Hiwonder TonyPi Pro (~$600)
- Significantly more affordable
- Programmable humanoid robot

### Important Warning:
The cheap kits (like Hiwonder) usually run on Raspberry Pi, which cannot run NVIDIA Isaac ROS efficiently. You would need to use these only for kinematics (walking) and use the Jetson kits for AI components.

## Option C: The "Premium" Lab (Sim-to-Real Specific)

### Hardware: Unitree G1 Humanoid
- **Target Audience**: Programs focused on sim-to-real transfer research
- **Capability**: One of the few commercially available humanoids that can actually walk dynamically
- **SDK Access**: Open enough for students to inject their own ROS 2 controllers

### Why G1 for Premium Labs:
- Direct sim-to-real transfer possible
- Advanced locomotion capabilities
- Realistic humanoid form factor
- Industry-relevant platform

## Lab Architecture for Successful Implementation

### Recommended Infrastructure:

| Component | Hardware | Function |
|-----------|----------|----------|
| Sim Rig | PC with RTX 4080 + Ubuntu 22.04 | Runs Isaac Sim, Gazebo, Unity, and trains LLM/VLA models |
| Edge Brain | Jetson Orin Nano | Runs the "Inference" stack. Students deploy their code here |
| Sensors | RealSense Camera + IMU | Connected to the Jetson to feed real-world data to the AI |
| Actuator | Unitree Go2 or G1 (Shared) | Receives motor commands from the Jetson |

## Considerations for Lab Setup

### Budget Planning:
- The "Proxy Approach" Option A is recommended for getting started
- Individual components can be acquired over time
- Sharing robots among students is viable with good scheduling

### Space Requirements:
- Adequate space for robot operation (clear area of at least 4m x 4m)
- Secure storage for expensive equipment
- Proper ventilation if running intensive simulations

### Safety Considerations:
- Safety protocols for robot operation
- Emergency stop procedures
- Proper supervision during operation

## Alternative: Cloud-Based Development

### When to Consider Cloud Options:
- If RTX-enabled workstations are not accessible
- For rapid deployment of virtual lab
- For students with weak local hardware

### Cloud Solution:
- AWS or Azure cloud instances with GPU support
  - Instance Type: AWS g5.2xlarge (A10G GPU, 24GB VRAM) or g6e.xlarge
- Software: NVIDIA Isaac Sim on Omniverse Cloud
- Cost: ~$1.50/hour (spot/on-demand mix) + storage costs
- Total estimated cost: ~$205 per quarter per student

### Local Bridge Hardware Still Required:
- Jetson Kit for physical deployment phase (~$700)
- One physical robot for final demo (~$3,000 for Unitree Go2 Standard)

## The Latency Trap (Hidden Cost)

### Important Consideration:
Simulating in the cloud works well, but controlling a real robot from a cloud instance is dangerous due to latency.

### Solution:
- Students train in the Cloud
- Download the model (weights) locally
- Flash it to the local Jetson kit

## Recommended Approach for Most Programs

For most educational programs, the recommended approach is:

1. **Start with Option A** (Proxy Approach) - Unitree Go2 Edu
2. **Implement Jetson Edge Kits** for each student/group
3. **Use high-performance workstations** with RTX GPUs for simulation
4. **Gradually add more advanced robots** as budget allows

This approach provides the best balance of educational value, cost-effectiveness, and safety while allowing students to learn all the core concepts of Physical AI and embodied intelligence.