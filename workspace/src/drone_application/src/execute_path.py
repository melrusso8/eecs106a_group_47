#!/usr/bin/env python
import rospy
import time
import tf2_ros
from std_msgs.msg import String
from std_msgs.msg import Empty
from geometry_msgs.msg import Twist



def land_drone():
        pub = rospy.Publisher("ardrone/land", Empty, queue_size=10 )
        rate = rospy.Rate(10) # 10hz
        t_end = time.time() + 7
        while time.time() < t_end:
	        pub.publish(Empty())
	        rate.sleep()

def distribute_seeds();
		######### do the thing and distribute seeds ##########



# send list of twists to drone to move between marked AR tag locations and distribute seeds
# Arguments:
#		tag_locations - a list body frames for every detected tag from mapping
def execute_path(tag_locations):
		#create publisher for drone commands
		pub = rospy.Publisher("cmd_vel", Twist, queue_size=10)
		tfBuffer = tf2_ros.Buffer()
  		tfListener = tf2_ros.TransformListener(tfBuffer)

  		#define rate for message transmission and area error for drone
        rate = rospy.Rate(10)
        area_error = 0.1
        x_diff = 1000
        y_diff = 1000
        K1 = 0.3
  		K2 = 1

  		# add condition for checking battery status out here somewhere...

        for goal_frame in tag_locations:

        	# move drone to position while the error between the drone's position and goal frame is above a certain threshold
        	while x_diff >= area_error and y_diff >= area_error:
        		try:
        			trans = tfBuffer.lookup_transform(---------, goal_frame, rospy.Time())

			      	# Process trans to get your state error
			      	x_diff = trans.transform.translation.x
			      	y_diff = trans.transform.translation.y

			      	# Generate a control command to send to the robot
			      	control_command = Twist()
			      	control_command.linear.x = x_diff*K1
			      	control_command.linear.y = y_diff*K2

			      	pub.publish(control_command)
			    except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
			      pass

			# Distribute seeds once drone has centered over tag
			distribute_seeds()

		# Land drone after last tag has been planted
		land_drone()

if __name__ == '__main__':
        rospy.init_node('drone_controller', anonymous=True)

        try:
          print("Starting Drone Control to Execute Path")
          execute_path(tag_locations) #### ---------> need to figure out where this variable will come from

        except rospy.ROSInterruptException:
          pass














