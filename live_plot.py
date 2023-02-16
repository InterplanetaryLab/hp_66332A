import csv
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

def auto_plot(i, filename):
    ax = []
    len_files = len(filename)
    ii = 0
    for i in filename:
        data = np.loadtxt(i, delimiter=",", skiprows=1)
        ax.append(plt.subplot(2,len_files, (ii+1)))
        ax.append(plt.subplot(2,len_files, (ii+2)))
        time = data[:,0]
        volt = data[:,1]
        curr = data[:,2]

        ax[ii].cla()
        ax[ii+1].cla()

        ax[ii].scatter(time,volt)
        ax[ii+1].scatter(time,curr)
        ax[ii].set_title("Filename: %s - Voltage Data Vs Time"%(i))
        ax[ii+1].set_title("Filename: %s - Current Data Vs Time"%(i))
        ax[ii].set_xlabel("Time (s)")
        ax[ii+1].set_xlabel("Time (s)")
        ax[ii].set_ylabel("Voltage (V)")
        ax[ii+1].set_ylabel("Current (A)")
        ii +=2

fig = plt.figure()
filename = "data3.csv"
filename2 = "data2.csv"
filenames = [filename]
ani = FuncAnimation(fig, auto_plot, interval=1000, fargs=(filenames,))
plt.show()
