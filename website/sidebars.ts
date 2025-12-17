import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */
const sidebars: SidebarsConfig = {
  // Manual sidebar configuration for the Physical AI & Humanoid Robotics book
  tutorialSidebar: [
    {
      type: 'category',
      label: 'Introduction',
      items: ['intro', 'why-physical-ai', 'learning-outcomes', 'weekly-breakdown', 'assessments'],
    },
    {
      type: 'category',
      label: 'Module 1: The Robotic Nervous System (ROS 2)',
      items: [
        'module1/intro',
        'module1/ros2-nodes-topics-services',
        'module1/rclpy-bridge',
        'module1/urdf-humanoids',
      ],
    },
    {
      type: 'category',
      label: 'Module 2: The Digital Twin (Gazebo & Unity)',
      items: [
        'module2/intro',
        'module2/gazebo-simulation',
        'module2/unity-rendering',
        'module2/sensor-simulation',
      ],
    },
    {
      type: 'category',
      label: 'Module 3: The AI-Robot Brain (NVIDIA Isaac™)',
      items: [
        'module3/intro',
        'module3/isaac-sim',
        'module3/isaac-ros',
        'module3/nav2-path-planning',
      ],
    },
    {
      type: 'category',
      label: 'Module 4: Vision-Language-Action (VLA)',
      items: [
        'module4/intro',
        'module4/voice-to-action',
        'module4/cognitive-planning',
        'module4/capstone-project',
      ],
    },
    {
      type: 'category',
      label: 'Hardware Requirements',
      items: [
        'hardware/intro',
        'hardware/workstation',
        'hardware/edge-kit',
        'hardware/lab-options',
      ],
    },
    {
      type: 'doc',
      id: 'architecture',
    },
    {
      type: 'doc',
      id: 'chatbot',
    },
    {
      type: 'doc',
      id: 'license',
    },
  ],
};

export default sidebars;
