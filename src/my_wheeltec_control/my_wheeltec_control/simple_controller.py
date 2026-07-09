#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class SimpleController(Node):
    """
    简单的小车控制器示例
    演示如何发布速度指令控制小车运动
    """
    def __init__(self):
        super().__init__('simple_controller')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.timer_callback)  # 10Hz
        self.counter = 0
        
    def timer_callback(self):
        """
        示例：小车向前走5秒，然后停止，然后左转，循环
        """
        twist = Twist()
        
        # 根据计数器决定运动状态
        if self.counter < 50:  # 前 5 秒 (50 * 0.1s)
            # 前进 0.2 m/s
            twist.linear.x = 0.2
            twist.angular.z = 0.0
        elif self.counter < 65:  # 接下来 1.5 秒左转
            twist.linear.x = 0.0
            twist.angular.z = 0.5  # 0.5 rad/s
        elif self.counter < 115:  # 接下来 5 秒后退
            twist.linear.x = -0.2
            twist.angular.z = 0.0
        elif self.counter < 130:  # 接下来 1.5 秒右转
            twist.linear.x = 0.0
            twist.angular.z = -0.5
        else:  # 停止
            twist.linear.x = 0.0
            twist.angular.z = 0.0
            self.counter = 0  # 重置循环
        
        self.publisher_.publish(twist)
        self.counter += 1
        
        if self.counter % 10 == 0:
            self.get_logger().info(f'发布速度: linear={twist.linear.x:.2f}, angular={twist.angular.z:.2f}')

def main(args=None):
    rclpy.init(args=args)
    node = SimpleController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
