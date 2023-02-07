from scipy import integrate
from scipy.fft import fft, fftfreq
from scipy.signal import blackman
from scipy import signal
from sklearn.preprocessing import MinMaxScaler
from plotUtil import plotAccels, plotData, plot3DVector, plotFiltVsUnfilt
from dataProcessing import cleanData, integ, lpf
import pandas as pd
import math
import os
import glob # unix style pathname pattern expansion
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

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
    return result

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
      
# display position change over time using graphic
# add vector to graphic with fixed positions for KSE, KNE, PHS, etc.


if __name__=="__main__":

    # get data
    datafiles = getCSV()
    
    # remove bad data and reformat index
    df = cleanData(datafiles[0])
    
    # TODO: Create a vector with x-y-z axes and map to new coordinate frame that matches hoistway

    # Confirm which axis aligns with hoistway (mechanics may shift box around as they work)
    print("Plotting all 3 acceleration axes")
    x_accel = df['xaccel']
    y_accel = df['yaccel']
    z_accel = df['zaccel']
    #plotAccels([x_accel, y_accel, z_accel])

    filteredData = lpf(y_accel)
    plotFiltVsUnfilt(y_accel, filteredData)
    #plot3DVector(x_accel[80000:85000], y_accel[80000:85000], z_accel[80000:85000])


    
    # given 3 pd Series, return the axis with the highest average
    # CHOOSE ACCEL AXIS WITH LARGEST AVERAGE

    accel = chooseAxis(x_accel, y_accel, z_accel)

    velocity = integ(accel)
    position = integ(velocity)
    
    print("Plotting...")
    plotData([accel, velocity, position])

    

    