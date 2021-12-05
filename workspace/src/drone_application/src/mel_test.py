#!/usr/bin/env python
import rospy
import time
from takeoff_move_land import move_forward, takeoff, turn_in_place
from std_msgs.msg import String
from std_msgs.msg import Empty
from geometry_msgs.msg import Twist

def map_the_grid(grid_width, grid_height, res=3):
    # assume drone is placed at the lower left corner of rectangular grid, facing long edge
    x = 0
    current_pos = (0,0)

    # take off
    takeoff()

    # traverse the grid
    while x < grid_width:
        move_forward(grid_height)
        turn_in_place(90)
        move_forward(res)
        x += res
        turn_in_place(90)
        current_pos = (x, grid_height)
        if x < grid_width:
            move_forward(grid_height)
            turn_in_place(-90)
            move_forward(res)
            x += res
            turn_in_place(-90)
            current_pos = (x, 0)

    # return drone to starting position
    if current_pos[1] == 0:
        # drone starts by facing long edge, at bottom right corner
        turn_in_place(-90)
        move_forward(x)
        turn_in_place(90)
    if current_pos[1] == grid_height:
        # drone starts by facing long edge, at top right corner
        move_forward(grid_height)
        turn_in_place(90)
        move_forward(x)
        turn_in_place(90)

    






