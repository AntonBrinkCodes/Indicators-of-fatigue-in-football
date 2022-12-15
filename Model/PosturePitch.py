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
    
    def __init__(self, acc_data=None, gyro_data=None, mag_data=None, quaternion = None, freq = 52, lr = 0.6, quat = None):
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
        r = R.from_quat(self.madgwick.Q)
        pitch = r.as_euler('xyz', degrees = True)[:,2]
        return pitch
        
    
    
    def updateIMU(self, acc, gyro):
            self.Q.append(self.madgwick.updateIMU(self.Q[self.Q.size],gyr = gyro, acc = acc), axis = 0)
            return self.getPP()[-1]
        
