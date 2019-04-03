#!/usr/bin/env python
import matplotlib.pyplot as plt
from tf.transformations import euler_from_quaternion, quaternion_from_euler
import math
import tf
import tf2_ros
import csv
import numpy as np


person_positions = [[2.513, -4.04, 0.0, 0.0, 0,0, -0.664, 0.748],
                   [0.55, -1.415, 0.0, 0.0, 0.0, 1.00, -0.019],
                   [1.086, -5.36, 0.0, 0.0, 0.0, 0.744, 0.668],
                   [-0.37, -2.309, 0.0, 0.0, 0.0, 0.725, 0.689],
                   [-0.373, -0.643, 0.0, 0.0, 0.0, -0.712, 0.702],
                   [-0.510, -4.047, 0.0, 0.0, 0.0, 0.070, 0.998],
                   [2.513, -4.04, 0.0, 0.0, 0.0, -0.664, 0.748]]

x_pose_person = []
y_pose_person = []
yaw_pose_person = []


for i in range(1, len(person_positions)):
    x_pose_person.append(person_positions[i][0])
    y_pose_person.append(person_positions[i][1])
    quaternion = [person_positions[i][3],person_positions[i][4],person_positions[i][5],person_positions[i][6]]
    (roll, pitch, yaw) = euler_from_quaternion (quaternion)
    yaw_pose_person.append(yaw)
    

with open('10_round_data.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    x = [] 
    y = []
    yaw = []
    for row in spamreader:
        x.append(row[0])
        y.append(row[1])
        yaw.append(row[2])
    
    # print(float(x[1]))
    # print(float(y[1]))
    count_chair = 0
    count_sofa = 0
    dist_sofa = []
    dist_chair = []
    angle_sofa = []
    angle_chair = []
    # distance = []
    # theta = []
    u = 0
    for i in range(1,len(x)-1):
        if u > 5:
            u = 0
        
        x1 = float(x[i])
        x2 = float(x_pose_person[u])
        y1 = float(y[i])
        y2 = float(y_pose_person[u])
        
        dist = math.sqrt( ((x2-x1)**2) + ((y2-y1)**2) )
        # distance.append(dist)

        # yaw1 = float(yaw[i])
        # yaw2 = float(yaw_pose_person[u])
        # angle = abs(y2 - y1) * 180 / math.pi

        # alternative for angle 
        angle = math.atan(abs((x2-x1)/(y2-y1)))
        angle = angle * 180 / math.pi # change to degree

        # theta.append(angle)
        u = u+1

        if angle > 60:
            dist_chair.append(dist)
            angle_chair.append(angle)
            count_chair = count_chair + 1
        else:
            dist_sofa.append(dist)
            angle_sofa.append(angle)
            count_sofa = count_sofa + 1

   
    fig = plt.figure()
    plt.plot(dist_sofa, angle_sofa, 'ro')
    plt.axis([0, 1, 0, 35])
   
    plt.xlabel('Distance (m) ', fontsize=18)
    plt.ylabel('Angle ( Degree ) ', fontsize=16)
    plt.grid(True, lw = 2, ls = ':', c = '.5')
    plt.rcParams.update({'font.size': 18})
    plt.show()
    fig.savefig('Result_Sofa.jpg')

       
    fig2 = plt.figure()
    plt.plot(dist_chair, angle_chair, 'ro')
    plt.axis([0, 1, 70, 100])
   
    plt.xlabel('Distance (m) ', fontsize=18)
    plt.ylabel('Angle ( Degree ) ', fontsize=16)
    plt.grid(True, lw = 2, ls = ':', c = '.5')
    plt.rcParams.update({'font.size': 18})
    plt.show()
    fig2.savefig('Result_Chair.jpg')


    print ("total sofa samples",count_sofa)
    print ("total chair samples",count_chair)