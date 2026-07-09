from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='my_wheeltec_control',
            executable='simple_controller',
            name='simple_controller',
            output='screen',
        ),
    ])
