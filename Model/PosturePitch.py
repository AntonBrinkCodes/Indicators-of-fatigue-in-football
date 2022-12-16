# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 08:55:38 2022
uses a Madgwick filter, implemented for Python from AHRS.
Calibrated to be used with a Movesense IMU device with Acceleration and Gyroscope
Attached to a persons torso to find the angle of their torso compared
from relative earth horizontal axis.


More information about Madgwick filters can be found at
https://ahrs.readthedocs.io/en/latest/filters/madgwick.html and

Sebastian Madgwick. An efficient orientation filter for inertial and 
inertial/magnetic sensor arrays. April 30, 2010. 
http://www.x-io.co.uk/open-source-imu-and-ahrs-algorithms/

AHRS is open-source. Their implementation of a Madgwick filter can be found at: 
https://github.com/Mayitzin/ahrs/blob/master/ahrs/filters/madgwick.py

@author: Anton Brink
"""

from ahrs.filters import Madgwick
import numpy as np
from scipy.spatial.transform import Rotation as R



class PosturePitch:
    
    def __init__(self, acc_data=None, gyro_data=None, mag_data=None, freq = 52, lr = 0.6, quat = None):
        """
        This this iniatier requires accelerometer and gyroscope data in a 
        nx3 np array. a baseline is calculated from the first few frames in the
        arrays using the Madgwick filter from AHRS. 
        Class can be initialized using a quaternion instead, the quaternion must
        have total length of 1.
        Parameters
        ----------
        acc_data : TYPE, optional
            A nx3 np array containing acceleration data in m/s^2.
        gyro_data : TYPE, optional
            A nx3 np array containing gyroscope data in radians/s.
        mag_data: TYPE, optional
            A nx3 np array containing magnetometer data in nT. Optional.
            NOTE: The default learning rate of 0.6 has not been calibrated 
            for use with magnetometer and may need to be changed for accurate results.
        freq : TYPE, optional
            Frequency. The default for a Movesense IMU is 52.
        lr : TYPE, optional
            Learning rate of the gradient descent algorithm. 
            The default is 0.6.
        quat : TYPE, optional
            The quaternion to be possibly be used to initialize class instead
            of np.arrays of acc, gyro and mag. Example: [1.0,0.0,0.0,0.0]

        Returns
        -------
        None. use method getPP() to get the posture pitch. If you want to look
        at more data you can use getQ() to get the whole orientation
        as a Rotation from a quaternion.

        """
        self.madgwick = Madgwick(gyr = gyro_data, acc=acc_data, mag=mag_data, frequency = freq, gain = lr, q0 = quat)
        self.Q = self.madgwick.Q
    
    
    
    def getPP(self):
        """
        Returns
        -------
        pitch : Float
            Returns the posture pitch as a List, each item in the List is the
            estimated posture pitch for that frame.

        """
        r = R.from_quat(self.Q)
        pitch = r.as_euler('xyz', degrees = True)[:,2]
        return pitch
        
    def getLastAsQuat(self):
        """
        Method to return latest estimated rotations as quaternions.
        Good to call for clearing data by creating a new instance of this class
        using this quaternion.
        Indented usage for keeping memory usage low.
        Returns
        -------
        TYPE
            Returns latest estimated orientation as a normalized quaternion.

        """
        return self.Q[-1]
    
    def getMean(self, start = None, end = None):
        """
        Get the mean of all Posture Pitches. Optionally specify between which indexes
        to calculate the mean between. 

        Parameters
        ----------
        start : TYPE, optional
            Start index to calculate mean from.
        end : TYPE, optional
            End index to calculate mean to.

        Returns
        -------
        TYPE
            The mean value of all Posture Pitches specified.

        """
       
        return self.getPP()[start:end].mean()
        

    
    def update(self, acc, gyro, mag=None):
        """
            Update the orientation with new data.
            Can be called as new IMU-data is sent from a IMU device.

        Parameters
        ----------
        acc : TYPE
        A 1x3 np array containing acceleration data in m/s^2.

        gyro : TYPE
            A 1x3 np array containing angular velocity data in rad/s.
        
        mag : TYPE, optional
            A 1x3 np array containing magnetometer data in nT.
            Only to be used if we are using a movesense device with 9DOF and
            magnetometer data is available.

        Returns
        -------
        TYPE
            The calculated orientation for this frame.

        """
        
        if(mag is None):
            self.Q[-1] = self.madgwick.updateIMU(self.Q[-1],gyr = gyro, acc = acc)
        else:
            self.Q[-1] = self.madgwick.updateMARG(self.Q[-1],gyr = gyro, acc = acc, mag = mag)

        return self.getPP()[-1]
    
        
        
