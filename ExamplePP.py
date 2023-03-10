# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 10:32:29 2022
Demonstrates the use of our Madgwick filter implementation to 
find PosturePitch using accelerometer
and Gyroscope data from a Movesense IMU6 device.

the json "running_example" is a short recording using the movesense device
of running -> walkin-> running with increased Posture Pitch.
The mp4 "Running_example" in the github is a video recording of this.

For this example. we use for-loop to simulate the streaming of data.

@author: Anton Brink
"""
import numpy as np
import matplotlib.pyplot as plt
import json

from Model.PosturePitch import PosturePitch as PP

#Helper functions to get data from example file
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
    acc = acc.transpose()
    gyro = gyro.transpose()

   # "Here we initialize a posturePitch object using the first second (we used 52Hz frequency) of IMU6 data"
    posturePitch = PP(gyro_data=gyro[:52], acc_data=acc[:52])
    
    
    
    #"To get the Posture Pitch we call getPP()" 
    pitch = posturePitch.getPP()
    plt.plot(np.arange(0,pitch.size), pitch)
    plt.title("Posture Pitch")
    plt.xlabel("frames")
    plt.ylabel("Torso degrees")
    plt.show()
    
   # "To simulate streaming data we loop through the remaining data and append this"
    #"to our numpy ndarray 'pitch' "
    #In real time, this could be called when a sensor sends new data instead of in a for loop
    for i in range(len(acc[52:,0])):
        pitch = np.append(pitch, posturePitch.update(gyro = gyro[i+52,:], acc = acc[i+52,:]))   
    plt.plot(np.arange(0,pitch.size), pitch)
    plt.title("Posture Pitch using first few frames")
    plt.xlabel("frames")
    plt.ylabel("Torso degrees")
    plt.show()

    #The posture pitch can also be initialized from a quaternion. The initial quaternion can be 
    #an assumed initial orientation, as shown below, and the filter will quickly correct this.
    posturePitchQuat = PP(gyro_data = gyro[:1], acc_data=acc[:1], quat = [ 0.0, 0.0, 0.7071068, 0.7071068 ])
    
    
    pitchQuat = posturePitchQuat.getPP()
    
    for i in range(len(acc[1:,0])):
        pitchQuat = np.append(pitchQuat, posturePitchQuat.update(gyro = gyro[i,:], acc = acc[i,:]))   
    plt.plot(np.arange(0,pitch.size), pitchQuat)
    plt.title("Posture Pitch from estimated quaternion")
    plt.xlabel("frames")
    plt.ylabel("Torso degrees")
    plt.show()
     
    # If your application does not require you to save posturePitch values for longer periods of time you can
    # Create a new PosturePitch instance with the last quaternion using getLastAsQuat():
    # Depending on your hardware this could be good to do at regular intervals 
    # to keep computation times and memory usage low. 
    
    posturePitchQuat = PP(gyro_data = gyro[:1], acc_data=acc[:1], quat = [ 0.0, 0.0, 0.7071068, 0.7071068 ])
    pitchQuat = posturePitchQuat.getPP()
    
    #Simulate performing this as in the example above, however we initiate a new
    #Posture Pitch halfway through.
    
    halfTime = int(len(acc[:,0])/2)
    #First half
    for i in range(len(acc[1:halfTime,0])):
        pitchQuat = np.append(pitchQuat, posturePitchQuat.update(gyro = gyro[i,:], acc = acc[i,:]))   
        
    # Initiate new PosturePitch
    posturePitchQuat = PP(gyro_data = gyro[:1], acc_data=acc[:1], quat = posturePitchQuat.getLastAsQuat())
    pitchQuat2 = posturePitchQuat.getPP()
    
    #Show the continued streaming of data:
    for i in range(len(acc[halfTime:,0])):
        pitchQuat2 = np.append(pitchQuat2, posturePitchQuat.update(gyro = gyro[i+halfTime-1,:], acc = acc[i+halfTime-1,:]))
    
    
    # To show:
    pitchQuat = np.append(pitchQuat, pitchQuat2)
    
    plt.plot(np.arange(0,pitchQuat.size), pitchQuat)
    plt.title("Posture Pitch thats been reset")
    plt.xlabel("frames")
    plt.ylabel("Torso degrees")
    plt.show()
    
    print(posturePitchQuat.getPP().size)
    
    # You can calculate the mean of the pitch between specified indexes by calling
    # PosturePitch.getMean(). Defaults to whole array if no indexes are
    # specififed.
    
    #Here is an example where we calculate the mean Posture Pitch of every second:
    meanArray =[posturePitchQuat.getMean(start = 0, end = 52)]
    x = [0]
    for i in map(lambda x: x+52 ,range(pitch.size-52)):
        if(i%52==0):
            x.append(i+52)
            meanArray.append(posturePitch.getMean(start = i, end = i+52))
            print(x)
    
    plt.plot(np.arange(0,pitchQuat.size), pitchQuat)
    plt.scatter(x, meanArray)
    plt.title("Posture Pitch thats been reset")
    plt.xlabel("frames")
    plt.ylabel("Torso degrees")
    plt.show()
                  
main()
