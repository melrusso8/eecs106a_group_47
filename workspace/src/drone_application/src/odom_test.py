#!/usr/bin/env python
import rospy
from std_msgs.msg import Empty
from ardrone_autonomy.msg import Navdata
from nav_msgs.msg import Odometry

def takeoff():
    pub = rospy.Publisher("ardrone/takeoff", Empty, queue_size=10, latch=True)

    rospy.Subscriber('ardrone/navdata', Navdata, navdata_listener_callback)
    rospy.Subscriber('ardrone/odometry', Odometry, odometry_listener_callback)

    rate = rospy.Rate(10)
    pub.publish(Empty())

def navdata_listener_callback(navdata):
    print('NAVDATA: \n %s \n\n' % navdata)

def odometry_listener_callback(odometry):
	print('ODOMETRY: \n %s \n\n' % odometry)

if __name__ == '__main__':
    rospy.init_node('odom_test', anonymous=True)
    takeoff()