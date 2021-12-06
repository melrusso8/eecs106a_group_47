#!/usr/bin/env python
import rospy
import time
from takeoff_move_land import move_forward, takeoff, turn_in_place
from std_msgs.msg import String
from std_msgs.msg import Empty
from geometry_msgs.msg import Twist
from ardrone_autonomy.msg import Navdata
from nav_msgs.msg import Odometry

def map_the_grid(grid_width, grid_height, x_step=3):
    # assume drone is placed at the lower left corner of rectangular grid, facing long edge
    rospy.Subscriber('ardrone/navdata', Navdata, navdata_listener_callback)
    rospy.Subscriber('ardrone/odometry', Odometry, odometry_listener_callback)

    x = 0
    drone_at_top = False
    turn_angle = 90

    # take off
    takeoff()

    # traverse the grid
    while x < grid_width:
        move_forward(grid_height)
        turn_in_place(turn_angle)
        move_forward(x_step)
        x += x_step
        turn_in_place(turn_angle)
        drone_at_top = not drone_at_top
        turn_angle = -turn_angle

    # return drone to starting position
    if not drone_at_top:
        # drone starts by facing long edge, at bottom right corner
        turn_in_place(-90)
        move_forward(x)
        turn_in_place(90)
    else:
        # drone starts by facing long edge, at top right corner
        move_forward(grid_height)
        turn_in_place(90)
        move_forward(x)
        turn_in_place(90)

def navdata_listener_callback(navdata):
    tag_locations = zip(tags_xc, tags_yc)
    # expressed in numbers between [0,1000]
    # need to convert to pixel units using camera resolution from camera_info topic

def odometry_listener_callback(odometry):
    drone_pose = odometry.pose.pose

if __name__ == '__main__':
        rospy.init_node('mapping', anonymous=True)