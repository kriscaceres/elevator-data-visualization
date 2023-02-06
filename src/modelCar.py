from scipy import integrate
from scipy.fft import fft, fftfreq
from scipy.signal import blackman
from scipy import signal
from sklearn.preprocessing import MinMaxScaler
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

"""

# used for ssh
matplotlib.use('TkAgg')


# import data from csv
def getCSV():
    path = "data/"
    extension = 'csv'
    os.chdir(path)
    result = glob.glob('*.{}'.format(extension)) # list of files, CWD = data/
    return result

# integrate to get velocity, then position
def integ(data):
    data_int = data.copy()
    result = np.array([])
    #time = np.linspace(0, data_int.size, data_int.size)
    for i in range(1, data_int.size, 1000):
        chunk_size = 1000
        if i+chunk_size >= data_int.size:
            chunk_size = data_int.size - i
        chunk_int = integrate.cumtrapz(data_int[i:i+chunk_size])
        result = np.append(result, chunk_int)
        
    data_int = integrate.cumtrapz(data_int, initial=0)
    return result, data_int

def cleanData(csvfile):
    print("Cleaning {} now".format(csvfile))
    try:
        data = pd.read_csv(csvfile)

        # Remove all bad values like NaN or 0.900.900
        data[data.columns[1:]] = data[data.columns[1:]].apply(pd.to_numeric, errors='coerce')

        # Remove all obvious outliers (e.g zaccel shouldn't be more than 2.5)
        zaccel_condition = (data['zaccel'] > -2.5) & (data['zaccel'] < 2.5)
        yaccel_condition = (data['yaccel'] > -2.5) & (data['yaccel'] < 2.5)
        xaccel_condition = (data['xaccel'] > -2.5) & (data['xaccel'] < 2.5)
        data = data[zaccel_condition & yaccel_condition & xaccel_condition]

        # update row numbering after filtering out rows
        data['row'] = np.arange(len(data)) 

        # take avg of accel data during off-peak to remove noise offset
        data['zaccel'] = data['zaccel'] - data['zaccel'][10000:70000].mean()

        return data
    except ValueError as ex:
        print(ex)

def normalize(df):
    scaler = MinMaxScaler(feature_range=(-0.55, 0.45))
    df_scaled = df.copy()
    df_scaled[['zaccel']] = scaler.fit_transform(df_scaled[['zaccel']])
    return df_scaled

def fft_df(df):
    data = df.copy()
    y = data['zaccel'].values
    y = y[120000:200000]
    # Number of sample points
    N = y.size
    # sample spacing (should be freq of data input, which is 2Hz)
    T = 1.0 / 2.0
    x = np.linspace(0.0, N*T, N, endpoint=False)

    xf = fftfreq(N,T)[:N//2] #// for floor, :N//2 is first index till N/2 floored
    yf = fft(y)
    w = blackman(N)
    ywf = fft(y*w)
    plt.semilogy(xf[1:N//2], 2.0/N * np.abs(yf[1:N//2]), '-b')
    plt.semilogy(xf[1:N//2], 2.0/N * np.abs(ywf[1:N//2]), '-r')
    plt.legend(['FFT', 'FFT w. window'])
    plt.grid()
    plt.show()

def hpf(df):
    # highest sampling rate is 0.5s or 2Hz
    # hpf with 2Hz
    fs = 2 #Hz
    #fp = 

# plot data
def plotData(data):

    time_0 = np.linspace(0, data[0].size, data[0].size)
    time_1 = np.linspace(0, data[1].size, data[1].size)
    time_2 = np.linspace(0, data[2].size, data[2].size)

    figs, axs = plt.subplots(3)
    figs.suptitle('Vanderbilt Z-Acceleration Integration')
    axs[0].plot(time_0, data[0], 'b')
    axs[1].plot(time_1, data[1], 'g')
    axs[2].plot(time_2, data[2], 'r')

    axs[0].title.set_text('Z-Accel')
    axs[1].title.set_text('Velocity')
    axs[2].title.set_text('Position')

    #axs[0].set_ylim([-2, 2])
   # axs[1].set_ylim([-10, 10])
    plt.autoscale(enable=True, axis='y')

    plt.show()

# display position change over time using graphic
# add vector to graphic with fixed positions for KSE, KNE, PHS, etc.


if __name__=="__main__":

    datafiles = getCSV()
    df = cleanData(datafiles[0])
    print("Finished cleaning data")
    accel = df['zaccel']
    print("Integrating for velocity")
    vel_chunked, vel = integ(accel)
    print("Integrating for position")
    pos_chunked_regvel, pos_regvel = integ(vel)
    pos_chunked_chunkedvel, pos_chunkedvel = integ(vel_chunked)
    print("Plotting chunked position with no chunked velocity")
    plotData([accel, vel, pos_chunked_regvel])
    print("Plotting chunked position with chunked vel")
    plotData([accel, vel_chunked, pos_chunked_chunkedvel])
    print("Plotting unchunked pos, unchunked vel")
    plotData([accel, vel, pos_regvel])

    #print("Computing FFT")
    #fft_df(df)
    