# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 10:32:29 2022
Demonstrates the use of our algorithms to find PosturePitch and Jumping Intensity
From IMU data.
We use for-loops to simulate the streaming of data.
@author: Anton Brink, Elsa Netz
"""
import numpy as np
import matplotlib.pyplot as plt
import json
import os
import io
from Model.PosturePitch import PosturePitch as PP
from ahrs.filters import Madgwick as mdw

" Helper functions to get data from example file"
def getXacc(jsonDict):
  dataList = jsonDict['data']
  xAcc = []
  for i in dataList:
      for j in range(4):
          xAcc.append(i.get('imu').get('ArrayAcc')[j].get('x'))
  return xAcc

def getYacc(jsonDict):
  dataList = jsonDict['data']
  yAcc = []
  for i in dataList:
      for j in range(4):
          yAcc.append(i.get('imu').get('ArrayAcc')[j].get('y'))
  return yAcc

def getZacc(jsonDict):
  dataList = jsonDict['data']
  zAcc = []
  for i in dataList:
      for j in range(4):
          zAcc.append(i.get('imu').get('ArrayAcc')[j].get('z'))
  return zAcc

def getXgyro(jsonDict):
  dataList = jsonDict['data']
  xGyro = []
  for i in dataList:
      for j in range(4):
          xGyro.append(np.deg2rad(i.get('imu').get('ArrayGyro')[j].get('x')))
  return xGyro

def getYgyro(jsonDict):
  dataList = jsonDict['data']
  yGyro = []
  for i in dataList:
      for j in range(4):
          yGyro.append(np.deg2rad(i.get('imu').get('ArrayGyro')[j].get('y')))
  return yGyro

def getZgyro(jsonDict):
  dataList = jsonDict['data']
  ZGyro = []
  for i in dataList:
      for j in range(4):
          ZGyro.append(np.deg2rad(i.get('imu').get('ArrayGyro')[j].get('z')))
  return ZGyro




def main ():
    with open('running_example.json', 'r') as imufile:
        imudata = json.load(imufile)

    acc = np.array([getXacc(imudata), getYacc(imudata), getZacc(imudata) ])
    gyro = np.array([getXgyro(imudata), getYgyro(imudata), getZgyro(imudata)])
  


    madgwick = PP(gyro_data=gyro.transpose(), acc_data=acc.transpose(), freq=52, lr = 0.6)
    print(madgwick.Q)
    
"    plt.plot(np.arange(0,pitch.size), pitch)"    
main()
