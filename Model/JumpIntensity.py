# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 09:13:43 2022
Used with Accelerometer in Movesense IMU device.
Uses combined acceleration from all axes to detect jump patterns and estimate
the flight times for each identified jump. 
A jump pattern is identified as two large peaks with a combined acceleration at
almost zero in between. The flight time is the time in between these peaks.

@author: Elsa Netz
"""

class JumpIntensity:
  def __init__(self,comAcc=None,freq=52,landThreshold=30,takeoffThreshold=15,flighttimeThreshold=0.5):
    """
    This this iniatier requires accelerometer data for x,y and z axis.
    Class can be initialized with different thresholds for the combined
    acceleration, as well as with different sample frequencies. 
    Parameters
    ----------
    comAcc : TYPE, optional
        A nx1 array containing the combined acceleration data in m/s^2.
    freq : TYPE, optional
        Frequency. The default for a Movesense IMU is 52.
    landThreshold : TYPE, optional
        An integer deciding a threshold for the landing peak.
        The default is 30 m/s^2.
    takeoffThreshold : TYPE, optional
        An integer deciding a threshold for the take-off peak.
        The default is 15 m/s^2.
    flighttimeThreshold : TYPE, optional
        An integer deciding a threshold for the maximum flighttime.
        The default is 0.5 s.
    Returns
    -------
    None. Use method findJump() to get the flight times for detected jumps.
    """

  def findJump(self):
    """
    Method to identify jumps and estimate the flight time for each jump found 
    within a window of frames.  
    Returns
    -------
    flighttimes : [Float]
        Returns the flight times as a List, each item in the List is the
        estimated flight time for jumps found in that window.
    """
    g = 9.81
    k = 3
    window = self.comAcc[:k]
    peaks = []
    timestamps = []
    flighttimes = []

    # Finds all peaks within the window. 
    # Saves them with their timestamp.
    for i in range(len(self.comAcc)-k):
      window = self.comAcc[i:(i+k)]
      if max(window) == window[1]:
        peaks.append(window[1])
        timestamps.append((i+k-1))

    # Compare peaks against thresholds to determine whether they represent 
    # a jump or not.
    # Saves and returns flight time (number of frames between peaks / frequency).
    for i in range(len(peaks)):
      if peaks[i] > self.landThreshold:
        temp = peaks[i::-1]
        for j in range(len(temp)-1):
          if temp[j+1] > self.takeoffThreshold and len(temp)>0:
            if ((timestamps[i]-timestamps[i-j-1])/self.freq)>self.flighttimeThreshold:
              flighttimes.append((timestamps[i]-timestamps[i-j-1])/self.freq)
              break
            else: 
              break

    return flighttimes