#!/usr/bin/env python
import rospy
import time
import tf2_ros
import sys
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
        pub.publish(Empty())

def land_drone():
		print("Landing drone")
		pub_land.publish(Empty())
		rate = rospy.Rate(10) # 10hz
		pub = rospy.Publisher("ardrone/land", Empty, queue_size=10, latch=True)
		duration = 3
		t_end = time.time() + duration
		while time.time() <  t_end:
			pub.publish(Empty())
#def distribute_seeds():
def execute_path(goal_frame):
		print("Taking off")
		takeoff()
		zero_out_params()
		time.sleep(7)
		print("Done taking off")
		    #create publisher for drone commands
		pub = rospy.Publisher("cmd_vel", Twist, queue_size=10)
		tfBuffer = tf2_ros.Buffer()
		tfListener = tf2_ros.TransformListener(tfBuffer)

  		  #define rate for message transmission and area error for drone
		rate = rospy.Rate(10)
		area_error = 0.05
		x_diff = 1000
		y_diff = 1000
		K1 = 0.2
		K2 = 0.2

		print("Entering while loop")
	    # move drone to position while the error between the drone's position and goal frame is above a certain threshold
		#while not rospy.is_shutdown():
		while abs(x_diff) >= area_error and abs(y_diff) >= area_error:
			try:
				#print("Doing try statement")
				trans = tfBuffer.lookup_transform("ardrone_base_link", goal_frame, rospy.Time())

            	# Process trans to get your state error
				x_diff = trans.transform.translation.x
				y_diff = trans.transform.translation.y

				print("x difference: " + str(x_diff))
				print("y difference: " + str(y_diff))
				print("")

            	# Generate a control command to send to the robot
				control_command = Twist()
				control_command.linear.x = x_diff*K1
				control_command.linear.y = y_diff*K2
				pub.publish(control_command)

			except tf2_ros.LookupException:
				print("LookupException Occured")
			except tf2_ros.ConnectivityException:
				print("ConnectivityException Occured")
			except tf2_ros.ExtrapolationException:
				print("ExtrapolationException Occured")
				pass

			time.sleep(0.1)

		print("Exiting while loop")
		land_drone()

if __name__ == '__main__':
        rospy.init_node('drone_controller', anonymous=True)

        try:
          print("Starting Drone Control to Execute Path")
          execute_path(sys.argv[1]) #### ---------> need to figure out where this variable will come from

        except rospy.ROSInterruptException:
          pass














