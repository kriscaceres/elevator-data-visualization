from scipy import integrate
from scipy.fft import fft, fftfreq
from scipy.signal import blackman, butter, filtfilt
from scipy import signal
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import math
import os
import glob # unix style pathname pattern expansion
import numpy as np
import matplotlib.pyplot as plt


# integrate to get velocity, then position
def integ(data):
    print("Integrating data...")
    try:
        #data_int = data.copy()
        result = np.array([])
        #time = np.linspace(0, data.size, data.size)
        for i in range(1, data.size, 100):
            chunk_size = 100
            if i+chunk_size >= data.size:
                chunk_size = data.size - i
            chunk_int = integrate.cumtrapz(data[i:i+chunk_size])
            result = np.append(result, chunk_int)
            
        #data_int = integrate.cumtrapz(data_int, initial=0)
        print("Integration successful.")
        return result #, data_int
    except Exception as ex:
        print("Issue with integration: \n", ex)

def cleanData(csvfile):
    print("Cleaning {} now...".format(csvfile))
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

        # ************  NOT NOISE -> BOX IS TILTED  ************
        # take avg of accel data during off-peak to remove noise offset
        data['zaccel'] = 9.8 * (data['zaccel'] - data['zaccel'][10000:70000].mean())
        data['xaccel'] = 9.8 * (data['xaccel'] - data['xaccel'][10000:70000].mean())
        data['yaccel'] = 9.8 * (data['yaccel'] - data['yaccel'][10000:70000].mean())

        print("Cleaning successful.")
        return data
    except ValueError as ex:
        print("Issue with cleaning data: \n", ex)

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

def lpf(data):
    # highest sampling rate is 0.5s or 2Hz
    # lpf with 2Hz
    fs = 2 #Hz, Sample frequency
    T = 86400 # Sample period
    total_samples = len(data)
    cutoff = 1
    nyq = 0.5 * fs
    order = 2
    n = int(T*fs)
    
    # butter lpf
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=True)
    y = filtfilt(b, a, data)
    return y
    #fp = 
