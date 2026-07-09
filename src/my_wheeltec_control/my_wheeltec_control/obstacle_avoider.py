#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Range

class ObstacleAvoider(Node):
    """
    基于超声波传感器的避障控制器
    订阅超声波数据，检测前方障碍物并自动避让
    """
    def __init__(self):
        super().__init__('obstacle_avoider')
        
        # 速度发布器
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        
        # 订阅超声波传感器数据
        # 根据车型不同，超声波传感器数量不同，这里订阅所有
        self.ultrasonic_distances = {}
        self.create_subscription(Range, '/ultrasonic_data_A', self.range_callback_A, 10)
        self.create_subscription(Range, '/ultrasonic_data_B', self.range_callback_B, 10)
        self.create_subscription(Range, '/ultrasonic_data_C', self.range_callback_C, 10)
        self.create_subscription(Range, '/ultrasonic_data_D', self.range_callback_D, 10)
        self.create_subscription(Range, '/ultrasonic_data_E', self.range_callback_E, 10)
        self.create_subscription(Range, '/ultrasonic_data_F', self.range_callback_F, 10)
        
        # 定时器，10Hz
        self.timer = self.create_timer(0.1, self.control_loop)
        
        # 避障阈值
        self.safe_distance = 0.4  # 米
        self.linear_speed = 0.15  # 前进速度 m/s

    def range_callback_A(self, msg): self.ultrasonic_distances['A'] = msg.range
    def range_callback_B(self, msg): self.ultrasonic_distances['B'] = msg.range
    def range_callback_C(self, msg): self.ultrasonic_distances['C'] = msg.range
    def range_callback_D(self, msg): self.ultrasonic_distances['D'] = msg.range
    def range_callback_E(self, msg): self.ultrasonic_distances['E'] = msg.range
    def range_callback_F(self, msg): self.ultrasonic_distances['F'] = msg.range

    def control_loop(self):
        twist = Twist()
        
        # 获取前方各传感器的距离
        front_a = self.ultrasonic_distances.get('A', 5.0)
        front_b = self.ultrasonic_distances.get('B', 5.0)
        front_c = self.ultrasonic_distances.get('C', 5.0)
        front_d = self.ultrasonic_distances.get('D', 5.0)
        
        # 前方任意传感器检测到障碍物
        obstacle_front = any(d < self.safe_distance for d in [front_a, front_b, front_c, front_d])
        
        if obstacle_front:
            # 前方有障碍物，根据左右距离决定转向
            left_dist = front_a + front_b  # 左侧大致距离
            right_dist = front_c + front_d  # 右侧大致距离
            
            if left_dist > right_dist:
                # 左侧空间更大，左转
                twist.angular.z = 0.5
                self.get_logger().info('检测到障碍物，左转避让')
            else:
                # 右侧空间更大，右转
                twist.angular.z = -0.5
                self.get_logger().info('检测到障碍物，右转避让')
            twist.linear.x = 0.0
        else:
            # 前方安全，前进
            twist.linear.x = self.linear_speed
            twist.angular.z = 0.0
        
        self.publisher_.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    node = ObstacleAvoider()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
