#!/usr/bin/env python

# from ipa_navigation_msgs.msg import StateEKF
from move_base_msgs.msg import MoveBaseGoal, MoveBaseAction
from actionlib_msgs.msg import GoalStatusArray
from geometry_msgs.msg import Pose

import rospy
from tf.transformations import euler_from_quaternion, quaternion_from_euler
import csv
import tf
import tf2_ros
import geometry_msgs.msg


class plotting_pose():
    def __init__(self):
        self.goal_count = 0
        self.pose_data = []
        self.robot_pose_data = []
        self.pose_data.append(["x","y","yaw","goal_number"])
        self.pose = []
        self.robot_pose = []
        self.goal_reached = False
        self.publish_goal = False
        self.sub = rospy.Subscriber("/move_base/status",GoalStatusArray,self.status_callback)
        self.sub2 = rospy.Subscriber("/robot_pose",Pose,self.pose_callback)
        self.human_pose = [[0,1,2],[1,2,1],[0,1,1],[1,2,0]] # just for testing
        self.test_robot_pose = [[2.0,0.0,3.0],[1.0,4.0,6.0],[2.0,3.0,0.0],[1.0,3.0,6.0]]
        

    def robot_pose_callback(self,msg):
        position = msg.pose.pose.position
        orientation = msg.pose.pose.orientation
        (roll, pitch, yaw) = euler_from_quaternion ([orientation.x,orientation.y,orientation.z,orientation.w])
        self.robot_pose = [position.x,position.y,yaw,self.goal_count]
        
    def pose_callback(self,msg):
        self.position = msg.position
        self.orientation = msg.orientation
        (roll, pitch, yaw) = euler_from_quaternion ([self.orientation.x,self.orientation.y,self.orientation.z,self.orientation.w])
        self.pose = [self.position.x, self.position.y, yaw,self.goal_count]
        
    def status_callback(self,msg):
        self.status = msg.status_list[0].status
        goal_sample = 2
        if self.goal_count < goal_sample:
            if self.status == 3 and not self.goal_reached:
                ######### when goal reached adding the pose to the data list
                self.goal_count += 1
                self.goal_reached = True
                print("goal_count :",self.goal_count)
                print("posenya : ",self.pose)
                self.pose_data.append(self.pose)
                self.robot_pose_data.append(self.robot_pose)
                self.robot_pose_data.append(self.human_pose[self.goal_count])

            elif self.status == 1 and self.goal_reached:
                ### reset the status
                self.goal_reached = False
        elif self.goal_count >= goal_sample and not self.publish_goal:
            print("final pose :",self.pose_data)
            self.write_to_csv(self.pose_data)
            self.publish_goal = True
        else:
            i = 0
            for i in range(0,goal_sample):
                self.pose_publish(self.pose_data[i+1],"pose "+str(i))
            # rospy.loginfo("Action finished")
            return

    def write_to_csv(self,pose):
        with open('data.csv', 'a+') as csvFile:
                writer = csv.writer(csvFile)
                for entry in pose:
                    rospy.logwarn(entry)
                    writer.writerows([entry])
                    rospy.loginfo("write successful")
                
    def pose_publish(self,pose, name):
        br = tf2_ros.TransformBroadcaster()
        t = geometry_msgs.msg.TransformStamped()
        t.header.stamp = rospy.Time.now()
        t.header.frame_id = "map"
        t.child_frame_id = name
        t.transform.translation.x = pose[0]
        t.transform.translation.y = pose[1]
        t.transform.translation.z = 0.0
        q = tf.transformations.quaternion_from_euler(0, 0, pose[2])
        t.transform.rotation.x = q[0]
        t.transform.rotation.y = q[1]
        t.transform.rotation.z = q[2]
        t.transform.rotation.w = q[3]

        br.sendTransform(t)

if __name__ == "__main__":
	rospy.init_node('plotting_pose')
	plot = plotting_pose()
	rospy.loginfo("pose analyzing mode starting")
	rospy.spin()
