#!/usr/bin/env python

from tf.transformations import euler_from_quaternion, quaternion_from_euler
import rospy
import tf
import tf2_ros
import csv
import numpy as np
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3



if __name__ == "__main__":
    rospy.init_node('pose_direction')
    odom_pub = rospy.Publisher("odom", Odometry, queue_size=50)
    rospy.loginfo("pose_direction node starting")
    while not rospy.is_shutdown():
        with open('10_round_data.csv', 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')
            x = [] 
            y = []
            yaw = []
            for row in spamreader:
                x.append(row[0])
                y.append(row[1])
                yaw.append(row[2])
            
            for i in range(1,len(x)-1):
                            # next, we'll publish the odometry message over ROS
                odom = Odometry()
                odom.header.stamp = rospy.Time.now()
                odom.header.frame_id = "map"
               
                q = tf.transformations.quaternion_from_euler(0, 0, float(yaw[i]))
                

                # set the position
                odom.pose.pose = Pose(Point(float(x[i]), float(y[i]), 0.), Quaternion(*q))

                # set the velocity
                odom.child_frame_id = "pose "+str(i)
                

                # publish the message
                odom_pub.publish(odom)



    rospy.spin()

