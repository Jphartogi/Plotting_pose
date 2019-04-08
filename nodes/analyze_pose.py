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
    dist_sofa2 = []
    dist_chair = []
    dist_chair2 = []
    dist_chair3 =[]
    angle_sofa = []
    angle_sofa2 = []
    angle_chair = []
    angle_chair2 = []
    angle_chair3 = []
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
        print " orang ke : ",u
        dist = math.sqrt( ((x2-x1)**2) + ((y2-y1)**2) )
        # distance.append(dist)
        
        # if u == 2:
        #     yaw1 = (float(yaw[i]) * 180 / math.pi) - 90  # change to degree
        # elif u == 0 or u == 3:
        #     yaw1 = (float(yaw[i]) * 180 / math.pi) + 90 
        # else:
        #     yaw1 = yaw1 = (float(yaw[i]) * 180 / math.pi)
        
        # this configuration is only for this data 
       
        yaw1 = (float(yaw[i]) * 180 / math.pi)

        yaw2 = float(yaw_pose_person[u])  * 180 / math.pi # change to degree

        if u == 0:
            angle =abs(abs(yaw2) - abs(yaw1))
        elif u == 1 or u == 4:
            angle = 180-(abs(yaw1))-(abs(yaw2))
        elif u == 2 or u == 3:
            angle = 180-(abs(yaw1))+(abs(yaw2))
        



        # # alternative for angle 
        # angle = math.atan(abs((x2-x1)/(y2-y1)))
        # angle = angle * 180 / math.pi # change to degree
        print("yaw data , yaw orang  :",yaw1,yaw2)
        print(" hasil pengurangan ",angle)
        print(" ")
        # theta.append(angle)
        u = u+1
        if u > 5:
            pass
        else:
            if angle > 60:
                
                if u == 1:
                    dist_chair.append(dist)
                    angle_chair.append(angle)
                    
                elif u == 3:
                    dist_chair2.append(dist)
                    angle_chair2.append(angle)
                    
                else:
                    dist_chair3.append(dist)
                    angle_chair3.append(angle)
                    count_chair = count_chair + 1

            else:
                
                if u == 2:
                    dist_sofa.append(dist)
                    angle_sofa.append(angle)
                    count_sofa = count_sofa + 1
             
                else:
                    dist_sofa2.append(dist)
                    angle_sofa2.append(angle)
      
    ########################### sofa #####################################
    fig = plt.figure()
    # plt.scatter(dist_sofa, angle_sofa, marker='o',c=10*10)
    sofa1 = plt.scatter(dist_sofa, angle_sofa,s=6000,c = "red",label='person 2')
    sofa2 = plt.scatter(dist_sofa2, angle_sofa2,s=6000,c = "blue",label='person 5')
    
    # plt.axis('tight')
    plt.axis([0.4, 0.95, 0, 25])
   
    plt.xlabel('Distance (m) ', fontsize=90)
    plt.ylabel('Angle ( Degree ) ', fontsize=90)
    plt.grid(True, lw = 2, ls = ':', c = '.5')
    plt.rcParams.update({'font.size': 90})
    plt.legend((sofa1,sofa2),
           ('person2', 'person5'),
           scatterpoints=1,
           loc='upper left',
           ncol=3,
           fontsize=30,
           bbox_to_anchor=(0, -0.25))
    plt.show()
    fig.savefig('Result_Sofa.jpg')




    ######################## chair #########################################


    fig2 = plt.figure()
    chair1 = plt.scatter(dist_chair, angle_chair, s=6000,c = "green",label='person 1')
    chair2 = plt.scatter(dist_chair2, angle_chair2, s=6000,c = "purple",label='person 3')
    chair3 = plt.scatter(dist_chair3, angle_chair3, s=6000,c = "yellow",label='person 4')
    plt.axis([0.4, 0.95, 75, 105])
    # plt.axis('tight')
    
   
    plt.xlabel('Distance (m) ', fontsize=90)
    plt.ylabel('Angle ( Degree ) ', fontsize=90)
    plt.grid(True, lw = 2, ls = ':', c = '.5')
    plt.rcParams.update({'font.size': 90})
    plt.legend((chair1,chair2,chair3),
           ('person1', 'person3','person4'),
           scatterpoints=1,
           loc='upper left',
           ncol=3,
           fontsize=30,
           bbox_to_anchor=(0, -0.25))
    plt.show()
    fig2.savefig('Result_Chair.jpg')


    print ("total sofa samples",count_sofa)
    print ("total chair samples",count_chair)
