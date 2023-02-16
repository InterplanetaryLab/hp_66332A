import csv
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation


def auto_plot(i):
    filename = "data.csv"
    time = []
    volt = []
    curr = []
    with open(filename, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        for row in csvreader:
            if ('Time' not in row[0]): # jank way of skipping first line
                if len(row) == 3:
                    time.append(float(row[0]))
                    volt.append(float(row[1]))
                    curr.append(float(row[2]))
    ax.cla()
    ax.scatter(time,volt)
    ax.scatter(time,curr)
    ax.set_title("Voltage and Current of Data Vs Time")
    ax.legend(["Voltage", "Current"])

fig = plt.figure()
ax = plt.subplot()

ani = FuncAnimation(fig, auto_plot, interval=1000)
plt.show()
