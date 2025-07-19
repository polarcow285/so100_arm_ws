import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import Header
import numpy as np
import time

class ManualControl (Node):
    def __init__(self):
        super().__init__("manual_control")

        self.publisher_ = self.create_publisher(JointState, "/isaac_joint_command", 12)

        self.joint_state = JointState()

        self.joint_state.name = ["Rotation", "Pitch", "Elbow", "Wrist_Pitch", "Wrist_Roll", "Jaw"]
        self.joint_state.position = [0.0] * len(self.joint_state.name)
        self.default_joints = [0,0,0,0,0,0]

        self.max_range = np.array(self.default_joints) + 0.3
        self.min_range = np.array(self.default_joints) - 0.3
        self.time_start = time.time()

        self.timer_ = self.create_timer(0.01, self.publish_joints)
        self.get_logger().info("manual_control has been started")

    def publish_joints(self):
        """joint_position = (
            np.sin(time.time() - self.time_start) * (self.max_range - self.min_range) * 0.5 + self.default_joints
        )

        self.joint_state.position = joint_position.tolist()
        self.set90()"""
        # Cycle the pose every few seconds
        self.set90()
        
        self.publisher_.publish(self.joint_state)
        self.get_logger().info("Published joints_state to joints_command topic")
    def set0(self):
        self.joint_state.position = [0.0,0.0,0.0,0.0,0.0,0.0]
    def set90(self):
        self.joint_state.position = [1.57,0.0,0.0,0.0,0.0,0.0]

def main(args=None):
    rclpy.init(args=args)

    node = ManualControl()
    
    rclpy.spin(node)

if __name__ == "main":
    main()
    