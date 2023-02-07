import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import plotly.express as px
import plotly.graph_objects as go

#matplotlib.use('TkAgg')

# plot data
def plotData(data):

    time_0 = np.linspace(0, data[0].size, data[0].size)
    time_1 = np.linspace(0, data[1].size, data[1].size)
    time_2 = np.linspace(0, data[2].size, data[2].size)

    figs, axs = plt.subplots(3)
    figs.suptitle('Vanderbilt Acceleration Integration')
    axs[0].plot(time_0, data[0], 'b')
    axs[1].plot(time_1, data[1], 'g')
    axs[2].plot(time_2, data[2], 'r')

    axs[0].title.set_text('Accel')
    axs[1].title.set_text('Velocity')
    axs[2].title.set_text('Position')

    #axs[0].set_ylim([-2, 2])
    #axs[1].set_ylim([-10, 10])
    plt.autoscale(enable=True, axis='y')

    plt.show()

def plotAccels(data):

    time = np.linspace(0, data[0].size, data[0].size)

    figs, axs = plt.subplots(3)
    figs.suptitle('Vanderbilt Acceleration Axes')
    axs[0].plot(time, data[0], 'b')
    axs[1].plot(time, data[1], 'g')
    axs[2].plot(time, data[2], 'r')

    axs[0].title.set_text('X-Accel')
    axs[1].title.set_text('Y-Accel')
    axs[2].title.set_text('Z-Accel')

    #axs[0].set_ylim([-2, 2])
   # axs[1].set_ylim([-10, 10])
    plt.autoscale(enable=True, axis='y')

    plt.show()

def plotFiltVsUnfilt(unfilt, filt):
    figs, axs = plt.subplots(2, sharex=True, sharey=True)

    axs[0].plot(unfilt, color='b', label='Unfiltered data')
    axs[1].plot(filt, color='r', label='Filtered data')
    plt.xlabel("Samples")
    plt.ylabel("m/s/s")
    plt.title("Unfiltered vs filtered acceleration signal")
    plt.show()


def plot3DVector(x,y,z):
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    
    ax.plot3D(x,y,z, 'red')
    ax.scatter3D(x,y,z, c=z, cmap='cividis')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    #ax.set_zlabel('z')
    plt.show()

# display position change over time using graphic
# add vector to graphic with fixed positions for KSE, KNE, PHS, etc.
