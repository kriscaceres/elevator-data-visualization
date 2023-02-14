
import time
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.patches as patches

from math import floor
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation

matplotlib.use('TkAgg')

# plot data
def plotData(data):

    time_0 = np.linspace(0, data[0].size, data[0].size)
    time_1 = np.linspace(0, data[1].size, data[1].size)
    time_2 = np.linspace(0, data[2].size, data[2].size)

    figs, axs = plt.subplots(3, sharex=True)
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
    
    ax.plot(x,y,z, 'red')
    #ax.scatter3D(x,y,z, c=z, cmap='cividis')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    #ax.set_zlabel('z')
    plt.show()

def plotCont(position):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    x= np.array([0])
    y= np.array([0])
    li, = ax.plot(x, y, 'r-')
    fig.canvas.draw()
    plt.show(block=False)
    plt.ion()
    for i in range(position.size):
        try:
            print("X: {}\nPosition: {}".format(i, position[i]))
            x = np.append(x, i)
            y = np.append(y, position[i])
            
            if i >= 100:
                x = np.delete(x, 0)
                y = np.delete(y, 0)
            
            # set the new data
            li.set_xdata(x)
            li.set_ydata(y)

            ax.relim()
            ax.autoscale_view(True, True, True)
            fig.canvas.draw()
            plt.pause(0.05)
        except KeyboardInterrupt:
            plt.close('all')
            break


def movingCar(position, floorTable, carWidth, carHeight):
    shaftHeight = len(floorTable)
    



    x = np.linspace(carWidth,carWidth,position.size) # will be only one value in array, until x-accel is included
    y = position
    #yaw = np.zeros(y.size)

    fig = plt.figure()
    #plt.axis('equal')
    ax = fig.add_subplot(111)
    ax.set_xlim(-carWidth, carWidth)
    ax.set_ylim(-1000, shaftHeight)
    #ax.autoscale_view(True, True, True)
    #ax.set_ylim(-4, 4)
    for index, entry in enumerate(floorTable):
        if entry is not None:
            ax.text((carWidth / 2) - 500, index, entry)
    

    patch = patches.Rectangle((0,0), 0, 0, fc='y')

    def init():
        ax.add_patch(patch)
        return patch,

    def animate(i):
        patch.set_width(carWidth)
        patch.set_height(carHeight)
        patch.set_xy([x[i], y[i]])
        #patch._angle = -np.rad2deg(yaw[i])
        return patch,

    anim = animation.FuncAnimation(fig, animate,
                                    init_func=init,
                                    frames=range(0, position.size, 100),
                                    interval=0.01,
                                    blit=True)
    #plt.rcParams['animation.ffmpeg_path'] = 'C:\\Users\\cacerekr\\ffmpeg-master-latest-win64-gpl\\bin\\ffmpeg.exe'
    #FFwriter=animation.FFMpegWriter(fps=360, extra_args=['-vcodec', 'libx264'])
    #anim.save('car_moving.mp4', writer=FFwriter)
    plt.grid(True)
    plt.show()
# display position change over time using graphic
# add vector to graphic with fixed positions for KSE, KNE, PHS, etc.
