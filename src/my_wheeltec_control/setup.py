from setuptools import setup
import os
from glob import glob

package_name = 'my_wheeltec_control'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='user',
    maintainer_email='user@example.com',
    description='自定义 Wheeltec 小车控制包',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'simple_controller = my_wheeltec_control.simple_controller:main',
            'auto_navigator = my_wheeltec_control.auto_navigator:main',
            'obstacle_avoider = my_wheeltec_control.obstacle_avoider:main',
        ],
    },
)
