#!/usr/bin/env python
import rospy
import time
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
	print("taking off")
	pub = rospy.Publisher("ardrone/takeoff", Empty, queue_size=10, latch=True)
	pub.publish(Empty())

def land():
	print("landing")
	pub = rospy.Publisher("ardrone/land", Empty, queue_size=10, latch=True)
	pub.publish(Empty())


def move_forward(vel):
	print("moving forward")
	pub = rospy.Publisher("cmd_vel", Twist, queue_size=10, latch=True)
	command_move = Twist()
	command_move.linear.x = vel
	pub.publish(command_move)

def move_laterally(vel, duration):
	#positive moves left, negative moves right
	print("moving laterally")
	time_end = time.time() + duration
	rate = rospy.Rate(10)

	while time.time() < time_end:
		pub = rospy.Publisher("cmd_vel", Twist, queue_size=10, latch=True)
		command_move = Twist()
		# command_move.linear.x = vel
		command_move.linear.y = vel
		pub.publish(command_move)
		rate.sleep()

def turn_in_place():
	print("turning in place")
	pub = rospy.Publisher("cmd_vel", Twist, queue_size=10, latch=True)
	command_rotate = Twist()
	command_rotate.angular.z = 0.1 # spin the drone
	pub.publish(command_rotate)


if __name__ == '__main__':
	rospy.init_node('movement_test', anonymous=True)

	try:
		takeoff()
		time.sleep(10)
	except rospy.ROSInterruptException:
		pass

	# try:
	# 	move_laterally(0.05, 10)
	# except rospy.ROSInterruptException:
	# 	pass

	try:
		land()
		time.sleep(5)
	except rospy.ROSInterruptException:
		pass


