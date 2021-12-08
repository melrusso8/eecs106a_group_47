#!/usr/bin/env python
import rospy
import time
import tf2_ros
import sys
from std_msgs.msg import String
from std_msgs.msg import Empty
from geometry_msgs.msg import Twist

def takeoff():
        pub = rospy.Publisher("ardrone/takeoff", Empty, queue_size=10, latch=True)
        rate = rospy.Rate(10)
        pub.publish(Empty())

def land_drone():
        pub_land = rospy.Publisher("ardrone/land", Empty, queue_size=10, latch=True)
        rate = rospy.Rate(10) # 10hz
        pub_land.publish(Empty())

#def distribute_seeds():
def execute_path(goal_frame):
        #takeoff()

		    #create publisher for drone commands
        pub = rospy.Publisher("cmd_vel", Twist, queue_size=10)
        tfBuffer = tf2_ros.Buffer()
        tfListener = tf2_ros.TransformListener(tfBuffer)

  		  #define rate for message transmission and area error for drone
        rate = rospy.Rate(10)
        area_error = 0.2
        x_diff = 1000
        y_diff = 1000
        K1 = 1
        K2 = 1
        print("Entering while loop")
    	# move drone to position while the error between the drone's position and goal frame is above a certain threshold
        #while x_diff >= area_error and y_diff >= area_error and not rospy.is_shutdown():
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
	      #r.sleep()

    		# Distribute seeds once drone has centered over tag
    		#distribute_seeds()

    		# Land drone after last tag has been planted
        #land_drone()

if __name__ == '__main__':
        rospy.init_node('drone_controller', anonymous=True)

        try:
          print("Starting Drone Control to Execute Path")
          execute_path(sys.argv[1]) #### ---------> need to figure out where this variable will come from

        except rospy.ROSInterruptException:
          pass














