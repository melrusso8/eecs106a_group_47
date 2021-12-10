#!/usr/bin/env python
import rospy
import time
import tf2_ros
import sys
import ctypes
import numpy as np
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
		pub_land.publish(Empty())
		rate = rospy.Rate(10) # 10hz
		pub = rospy.Publisher("ardrone/land", Empty, queue_size=10, latch=True)
		duration = 3
		t_end = time.time() + duration
		while time.time() <  t_end:
			pub.publish(Empty())


def execute_path(goal_frame):
		print("______ Planting " + goal_frame + " ______")
		print("")

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

		#print("Exiting while loop")
		print("distributing seeds...")
		print("")
		time.sleep(5)



if __name__ == '__main__':
		#intialize drone controller node
        rospy.init_node('drone_controller', anonymous=True)

        #create list of tags to plant
        tags_to_plant = [0] * (len(sys.argv) - 1)

        for idx in range(1, len(sys.argv)):
        	tags_to_plant[idx - 1] = sys.argv[idx]

    	print("the tags that will be planted are: " + str(tags_to_plant) + "(according to shortest path)")
        

        #create list according to shortest path
        tags_to_plant_shortest = [0] * len(tags_to_plant)
        total_num_frames = len(tags_to_plant)
        tags_used = [0] * len(tags_to_plant)

        curr_frame = "ardrone_base_link"
    	curr_closest_tag = ""

        tfBuffer1 = tf2_ros.Buffer()
        tfListener1 = tf2_ros.TransformListener(tfBuffer1)

        #calculate order of tags to be visited depending on distance
        idx = 0
        while (idx < total_num_frames):
			curr_closest_dist = 1000 #reset curr_closest_dist

			for tag in tags_to_plant:
				invalid_trans = True

				if (tag not in tags_used and tag != curr_frame):
					while invalid_trans:
						try:
							print("curr frame: " + curr_frame)
							print("tag frame: " + tag)
							print("")

							trans1 = tfBuffer1.lookup_transform(curr_frame, tag, rospy.Time())
							invalid_trans = False
							x_diff = trans1.transform.translation.x
							y_diff = trans1.transform.translation.y
							total_dist = np.sqrt(x_diff**2 + y_diff**2)
							print(total_dist)
							#print("tootal distance for " + tag + " is " + str(total_dist))

							# set new closest distance and tag to keep track of
							if(total_dist < curr_closest_dist):
								curr_closest_tag = tag
								curr_closest_dist = total_dist

						except tf2_ros.LookupException:
							print("LookupException Occured")
						except tf2_ros.ConnectivityException:
							print("ConnectivityException Occured")
						except tf2_ros.ExtrapolationException:
							print("ExtrapolationException Occured")
							pass

			tags_to_plant_shortest[idx] = curr_closest_tag
			curr_frame = curr_closest_tag
			tags_used[idx] = curr_frame
			idx = idx + 1

        try:
        	#takeoff and zero out parameters for hovering
			print("********** Taking off **********")
			print("")
			print(tags_to_plant_shortest)
			#takeoff()
			zero_out_params()
			print("********** Done taking off **********")
			print("")
			time.sleep(4)

			#move to each tag in order of input: locate and distribute seeds
			print("**** Starting Drone Control to Execute Path ****")
			print("")
			time.sleep(4)
			for tag in tags_to_plant_shortest:
				execute_path(tag)

			#land the drone once all tags are accounted for
			print("********** landing drone **********")
			print("")
			#land_drone()

        except rospy.ROSInterruptException:
          pass














