# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 12:43:21 2022
Demonstrates the use of our jump identifying algorithm to 
find PosturePitch using accelerometer data from a Movesense IMU6 device.
The json "run_jump_example" is a short recording using the Movesense device
of standing, running and jumping (twice) at random times.
For this example we use for-loop to simulate the streaming of data.
@author: Elsa Netz
"""

import matplotlib.pyplot as plt
import matplotlib.axes as axes
import json
import math

from Model.JumpIntensity import JumpIntensity as JI

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

def getTimeVector(V):
  timeVector = [0]*len(V)
  j = 0
  for i in range(len(timeVector)):
    timeVector[i] = j
    j = j+1
  
  return timeVector

def getComAcc(xAcc,yAcc,zAcc):
  comAcc = [0]*len(xAcc)
  g = 9.81 #m/s^2
  a = 0
  for i in range(len(xAcc)):
    comAcc[a] = math.sqrt(0.25*math.pow(xAcc[a],2)+2.5*math.pow(yAcc[a],2)+0.25*math.pow(zAcc[a],2))-g
    a = a+1
  
  return comAcc

def main():
  with open('run_jump_imu.json', 'r') as imufile:
    imudata = json.load(imufile)
  
  comAcc = getComAcc(getXacc(imudata),getYacc(imudata),getZacc(imudata))

  # "Here we initialize a JumpIntensity object using the first second (we used 52Hz frequency) of IMU6 data"
  jumps = JI(comAcc = comAcc[:52])

  # "To get the flight times we call findJump() 

  # "To simulate streaming data we loop through the data with a sliding window "
  # " and append all jumps found during each 1 second window ('TOF') to our "
  # " 'TOF10min' array to get the total intensity over 10 minutes."
  # " To 'TOF10min, both the individual flight times and the sum of them are saved."
  # " For this example, this is added each second, due to the short sample time."
  #In real time, this could be called when a sensor sends new data instead of in a for loop

  kTOF = 52 # frames = 1s
  windowTOF = comAcc[:kTOF]
  TOFs = []
  TOF10min = []

  for i in range(len(comAcc)-kTOF):
    windowTOF = comAcc[i:(i+kTOF)]
    TOF = jumps.findJump(windowTOF)
    for j in range(len(TOF)):
      if (TOF[j] not in TOFs) and (TOF[j] not in TOF10min[-1]):
        TOFs.append(TOF[j])
    if i%52 == 0: # change 52 to 10 min = 31200 frames for saving every 10 minutes
      TOF10min.append(sum(TOFs))
      TOF10min.append(TOFs)
      TOFs = []
  
  # To show Jump Intensity for each second of the sample:
  t = getTimeVector(TOF10min[::2]) 
  # creates time vector for every other element in 'TOF10min', since the other
  # elements are arrays of individual flight times and we only want the sums

  fig, ax = plt.subplots()
  ax.bar(t, height = TOF10min[::2], width = 0.1)
  ax.set_xticks([0,1,2,3,4,5,6,7])
  ax.set_xticklabels(['$1$','$2$','$3$','$4$','$5$','$6$','$7$'])
  plt.title("Jump Intensity")
  plt.xlabel("jumps")
  plt.ylabel("jump intensity")
  plt.show()

main()