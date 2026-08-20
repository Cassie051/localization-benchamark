#!/usr/bin/env python3

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    project_dir = get_package_share_directory('orb_slam3_bringup')
    
    # --- ADD THIS: Path to your ORBvoc.txt ---
    # UPDATE THIS PATH to wherever your ORBvoc.txt is actually saved!
    # Common location: '/home/pc/Doktorat/other/orbslam_ws/src/orb_slam3/Vocabulary/ORBvoc.txt'
    voc_file_path = '$BENCHMARK_DIR/src/orb_slam3_ros/orb_slam3_ros/modules/ORB_SLAM3/Vocabulary/ORBvoc.txt'

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_imu_data',
            default_value='True',
            description='Use IMU data?'
        ),
        
        # ORB-SLAM3 Monocular tracking node
        Node(
            package='orb_slam3_ros',
            executable='orb_slam3_ros_mono',
            output='screen',
            parameters=[{
                'voc_file': voc_file_path,
                'settings_file': os.path.join(project_dir, 'param', 'oxford_mono_inertial.yaml'),
                'world_frame_id': 'map',
                'use_sim_time': True
            }],
            remappings=[
                ('/image_raw', '/camera/image_raw')
            ],
            condition=UnlessCondition(LaunchConfiguration('use_imu_data')),
        ),

        # ORB-SLAM3 Monocular Inertial tracking node
        Node(
            package='orb_slam3_ros',
            executable='orb_slam3_ros_mono_imu',
            output='screen',
            parameters=[{
                'voc_file': voc_file_path,
                'settings_file': os.path.join(project_dir, 'param', 'oxford_mono_inertial.yaml'),
                'world_frame_id': 'map',
                'use_sim_time': True
            }],
            remappings=[
                ('/image_raw', '/camera/image_raw'),
                ('/imu', '/alphasense_driver_ros/imu')
            ],
            condition=IfCondition(LaunchConfiguration('use_imu_data')),
        ),
    ])