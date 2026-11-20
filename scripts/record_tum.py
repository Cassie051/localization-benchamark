#!/usr/bin/env python3

import sys
import time
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseStamped

class TumRecorder(Node):
    def __init__(self, topic_name, output_file, msg_type):
        super().__init__('tum_recorder_node')
        self.output_file = output_file
        self.file_handle = open(self.output_file, 'w')
        
        self.has_started = False
        self.last_msg_time = time.time()
        self.start_time = time.time()
        
        self.timeout_first_msg = 30.0  
        self.timeout_silence = 5.0     
        
        if msg_type == "PoseStamped":
            self.subscription = self.create_subscription(
                PoseStamped, topic_name, self.pose_callback, 10)
        else:
            self.subscription = self.create_subscription(
                Odometry, topic_name, self.odom_callback, 10)
            
        self.timer = self.create_timer(1.0, self.check_heartbeat)
        self.get_logger().info(f"Listening to {topic_name} ({msg_type}). Waiting for data...")

    def write_tum(self, stamp, pose):
        self.has_started = True
        self.last_msg_time = time.time()
        
        timestamp = stamp.sec + (stamp.nanosec / 1e9)
        tx, ty, tz = pose.position.x, pose.position.y, pose.position.z
        qx, qy, qz, qw = pose.orientation.x, pose.orientation.y, pose.orientation.z, pose.orientation.w
        
        line = f"{timestamp:.6f} {tx:.6f} {ty:.6f} {tz:.6f} {qx:.6f} {qy:.6f} {qz:.6f} {qw:.6f}\n"
        self.file_handle.write(line)

    def odom_callback(self, msg):
        self.write_tum(msg.header.stamp, msg.pose.pose)

    def pose_callback(self, msg):
        self.write_tum(msg.header.stamp, msg.pose)

    def check_heartbeat(self):
        current_time = time.time()
        if not self.has_started:
            if (current_time - self.start_time) > self.timeout_first_msg:
                self.get_logger().error(f"Timeout: No data on {self.subscription.topic_name}.")
                raise SystemExit
        else:
            if (current_time - self.last_msg_time) > self.timeout_silence:
                self.get_logger().info(f"Topic silent for {self.timeout_silence}s. Finished!")
                raise SystemExit

def main(args=None):
    if len(sys.argv) < 3:
        print("Usage: python3 record_tum.py <topic_name> <output_file> [msg_type: Odometry|PoseStamped]")
        sys.exit(1)

    topic_name = sys.argv[1]
    output_file = sys.argv[2]
    msg_type = sys.argv[3] if len(sys.argv) > 3 else "Odometry"

    rclpy.init(args=args)
    recorder = TumRecorder(topic_name, output_file, msg_type)

    try:
        rclpy.spin(recorder)
    except SystemExit:
        pass
    finally:
        recorder.file_handle.close()
        recorder.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()