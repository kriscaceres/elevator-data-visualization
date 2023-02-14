import glob  # unix style pathname pattern expansion
import os
from Car import Car 
from Shaft import Shaft

import matplotlib
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import animation
from scipy import integrate, signal
from scipy.fft import fft, fftfreq
from scipy.signal import blackman
from sklearn.preprocessing import MinMaxScaler

import plotUtil
from dataProcessing import cleanData, integ, lpf

"""
This tool will model the car moving through a hoistway using data collected from Vanderbilt.
FUTURE: use for test tower, batch processing.
Algorithm: 
1. Read in data from csv into pandas dataframe
2. Clean data from bad outliers
3. Shift data in y-direction in case of noise 
4. Separate data in chunks to lower integration error
5. Integrate each chunk
6. Append the integration results into one series/array
7. Plot the results
    
# TODO: Create a vector with x-y-z axes and map to new coordinate frame that matches hoistway

"""

# import data from csv
def getCSV():
    path = "data/"
    extension = 'csv'
    os.chdir(path)
    result = glob.glob('*.{}'.format(extension)) # list of files, CWD = data/
    return 

def floorTable():
    # KSE magnets, KNE switches, floor levels, PHS, PHSB, PHNRU/D, PHUET 
    # floor levels
    '''
    how to handle this:
    
    '''
def chooseAxis(x,y,z):
    avg_x = x.nlargest().mean()
    avg_y = y.nlargest().mean()
    avg_z = z.nlargest().mean()
    print("Avg x: ", avg_x)
    print("Avg y: ", avg_y)
    print("Avg z: ", avg_z)
    if avg_z >= avg_x and avg_z >= avg_y:
        return z
    if avg_y >= avg_x and avg_y >= avg_z:
        return y
    if avg_x >= avg_y and avg_x >= avg_z:
        return x
      
# add vector to graphic with fixed positions for KSE, KNE, PHS, etc.


if __name__=="__main__":

    carN = Car("S3350", 1.02, 0.80, width=2058, depth=1332, height=2362)

    BUFFER = 600
    KNE_D = BUFFER + 500
    PHS_1 = KNE_D + carN.height + 250
    PHS_2 = PHS_1 + 2890
    KNE_U = PHS_2 + 250
    KSE_D = PHS_1 + 500
    KSE_U = KSE_D + 50
    SHAFT_HEAD = KNE_U + 1000

    # total shaft = 6m
    floorTableN = [("BUFFER", BUFFER), ("KNE_D", KNE_D), 
                   ("PHS_1", PHS_1), ("PHS_2", PHS_2),
                   ("KNE_D", KNE_D), ("KNE_U", KNE_U),
                   ("KSE_D", KSE_D), ("KSE_U", KSE_U),
                   ("SHAFT_HEAD", SHAFT_HEAD)]

    shaftN = Shaft(height=SHAFT_HEAD, floorTable=floorTableN)
    print(shaftN.floor_table)

    # get data
    #datafiles = getCSV()

    # csvfile
    csvfile = 'az_102mps_poweroff.csv'
    #csvfile = 'pos_z.csv'
    csvlocation = os.path.join('data', csvfile)

    df = pd.read_csv(csvlocation)
    print(df)

    accel = df['zaccel']
    #vel_enc = df['vel_enc']
    # given 3 pd Series, return the axis with the highest average
    # CHOOSE ACCEL AXIS WITH LARGEST AVERAGE

    #accel = chooseAxis(x_accel, y_accel, z_accel)
    #accel = z_accel
    vel_z = integ(accel - accel.mean())
    pos_z = integ(vel_z)
    #pos_enc = integ(vel_enc[57000:69600])
    #pos_z = df['pos_z']
    plotUtil.movingCar(pos_z, shaftN.floor_table, carN.width, carN.height)

    #print("Plotting...")
    ###plotUtil.plotData([accel, vel_z, pos_z])
        

        