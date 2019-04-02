#!/usr/bin/env python
import matplotlib.pyplot as plt
import math

import csv

with open('data.csv', 'rb') as csvfile:
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

    distance = []
    theta = []
    for i in range(1,len(x)-1):
        mod = i % 2
        if mod > 0:
            x1 = float(x[i])
            x2 = float(x[i+1])
            y1 = float(y[i])
            y2 = float(y[i+1])
            dist = math.sqrt( ((x2-x1)**2) + ((y2-y1)**2) )
            distance.append(dist)

            yaw1 = float(yaw[i])
            yaw2 = float(yaw[i+1])
            angle = abs(y2 - y1)
            theta.append(angle)

   
    print(distance)

    plt.plot(distance, theta, 'ro')
    plt.axis([0, 6, 0, 20])
    plt.show()
        