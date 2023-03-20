import matplotlib.pyplot as plt
import numpy as np

class SensorVisualizer:

    def __init__(self, q_sensor, title="Sensor", plot_x_size=500, ylim=100):
        # initialize the plot
        self.fig, self.ax = plt.subplots(1, 1, figsize=(9, 3), dpi=80)
        self.x = np.arange(0, plot_x_size)
        self.data = list([])
        self.lines = list([])
        for i, (c,label) in enumerate(zip(['r','g','b'], ['x','y','z'])):
            self.data.append(np.zeros(plot_x_size))
            self.lines.append(self.ax.plot(self.x, self.data[i], color=c, label=label)[0])
        self.ax.set_title(title, fontsize=20)
        self.ax.set_xlabel("Samples", fontsize=12)
        self.ax.set_ylabel("Values", fontsize=12)
        self.ax.set_xlim([0, plot_x_size])
        self.ax.set_ylim([-ylim, ylim])
        plt.tight_layout()
        plt.legend(loc='upper right')
        plt.pause(0.0000001)
        # init the queue
        self.q = q_sensor
        self.counter = 0

    def update(self):
        raw = self.q.get()[:-3]  # Get data from the queue
        for i in [0,1,2]:
            self.data[i] = np.hstack(([raw[i]], self.data[i]))[:-1]  # x
        self.counter += 1
        if self.counter == 10:  # update plot every 10 samples
            for i in [0, 1, 2]:
                self.lines[i].set_ydata(self.data[i])
            self.counter = 0
            plt.pause(0.0000000001)

def plottingThread(q_sensor,  title="Accelerometer", plot_x_size=500, ylim=100):
    viz = SensorVisualizer(q_sensor, title=title, plot_x_size=plot_x_size, ylim=ylim)
    while True:
        viz.update()