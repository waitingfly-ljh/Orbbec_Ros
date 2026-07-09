#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import math
import time

class AutoNavigator(Node):
    """
    自动导航控制器
    读取里程计信息，使小车按预设路径点移动
    """
    def __init__(self):
        super().__init__('auto_navigator')
        
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.odom_sub = self.create_subscription(Odometry, '/odom', self.odom_callback, 10)
        self.timer = self.create_timer(0.1, self.control_loop)
        
        # 当前位姿
        self.current_x = 0.0
        self.current_y = 0.0
        self.current_yaw = 0.0
        self.odom_ready = False
        
        # 预设路径点 (x, y) 单位：米
        self.waypoints = [
            (1.0, 0.0),   # 前进1米
            (1.0, 1.0),   # 左转再前进1米
            (0.0, 1.0),   # 左转再前进1米
            (0.0, 0.0),   # 回到起点
        ]
        self.current_waypoint = 0
        
        # 控制参数
        self.linear_speed = 0.15
        self.angular_speed = 0.5
        self.distance_tolerance = 0.1  # 到达目标点容差
        self.angle_tolerance = 0.1     # 角度容差 (rad)

    def odom_callback(self, msg):
        self.current_x = msg.pose.pose.position.x
        self.current_y = msg.pose.pose.position.y
        
        # 从四元数提取偏航角
        q = msg.pose.pose.orientation
        siny = 2.0 * (q.w * q.z + q.x * q.y)
        cosy = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)
        self.current_yaw = math.atan2(siny, cosy)
        self.odom_ready = True

    def control_loop(self):
        if not self.odom_ready:
            self.get_logger().info('等待里程计数据...')
            return
        
        if self.current_waypoint >= len(self.waypoints):
            # 所有路径点已走完，停止
            self.publisher_.publish(Twist())
            self.get_logger().info('已到达所有路径点!')
            return
        
        target_x, target_y = self.waypoints[self.current_waypoint]
        
        # 计算到目标点的距离和角度
        dx = target_x - self.current_x
        dy = target_y - self.current_y
        distance = math.sqrt(dx**2 + dy**2)
        target_angle = math.atan2(dy, dx)
        angle_diff = target_angle - self.current_yaw
        
        # 归一化角度到 [-pi, pi]
        angle_diff = math.atan2(math.sin(angle_diff), math.cos(angle_diff))
        
        twist = Twist()
        
        if distance < self.distance_tolerance:
            # 到达当前路径点，切换到下一个
            self.get_logger().info(f'到达路径点 {self.current_waypoint+1}: ({target_x:.2f}, {target_y:.2f})')
            self.current_waypoint += 1
        elif abs(angle_diff) > self.angle_tolerance:
            # 先转向目标方向
            twist.angular.z = self.angular_speed if angle_diff > 0 else -self.angular_speed
        else:
            # 前进
            twist.linear.x = min(self.linear_speed, distance)
        
        self.publisher_.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    node = AutoNavigator()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
