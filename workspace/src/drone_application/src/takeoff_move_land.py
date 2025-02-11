#!/usr/bin/env python
import rospy
import time
from std_msgs.msg import String
from std_msgs.msg import Empty
from geometry_msgs.msg import Twist


def zero_out_params():
		pub = rospy.Publisher("cmd_vel", Twist, queue_size=10, latch=True)
		rate = rospy.Rate(10)
		command_zero = Twist()
		command_zero.angular.x = 0
		command_zero.angular.y = 0
		command_zero.angular.z = 0
		command_zero.linear.x = 0
		command_zero.linear.y = 0
		command_zero.linear.z = 0
		pub.publish(command_zero)

def takeoff():
        pub = rospy.Publisher("ardrone/takeoff", Empty, queue_size=10, latch=True)
        rate = rospy.Rate(10)
        t_end = time.time() + 7
        #while time.time() < t_end:
        pub.publish(Empty())

def turn_in_place():
        pub = rospy.Publisher("cmd_vel", Twist, queue_size=10, latch=True)
        rate = rospy.Rate(10)
        command_rotate = Twist()
        command_rotate.angular.z = 0.3 # spin the drone
        t_end = time.time() + 3
        #while time.time() < t_end:
        pub.publish(command_rotate)
        #rate.sleep()

def move_forward():
        pub = rospy.Publisher("cmd_vel", Twist, queue_size=10, latch=True)
        rate = rospy.Rate(10)
        command_move = Twist()
        command_move.linear.x = 0.1 # move drone forwards

        pub.publish(command_move)
        #rate.sleep()

def land():
        pub = rospy.Publisher("ardrone/land", Empty, queue_size=10, latch=True)
        rate = rospy.Rate(10) # 10hz
        t_end = time.time() + 7
        #while time.time() < t_end:
        pub.publish(Empty())
        #rate.sleep()

if __name__ == '__main__':
        rospy.init_node('drone_test1', anonymous=True)

        try:
          print("Taking off")
          takeoff()
          time.sleep(2)
        except rospy.ROSInterruptException:
          pass 

        # try:
        #   print("zeroing out angular x and angular y")
        #   zero_out_params()
        #   #time.sleep(7)
        # except rospy.ROSInterruptException:
        #   pass
        try:
          print("Turning in place")
          turn_in_place()
          time.sleep(4)
        except rospy.ROSInterruptException:
          pass
        try:
          print("Moving forward")
          move_forward()
          time.sleep(5)
        except rospy.ROSInterruptException:
          pass
        try:
          print("Landing")
          land()
          time.sleep(3)
        except rospy.ROSInterruptException:
          pass