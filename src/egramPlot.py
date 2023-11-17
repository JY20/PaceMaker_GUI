import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class updateable_matplotlib_plot():
    def __init__(self, canvas) -> None:
        self.fig_agg = None
        self.figure = None
        self.canvas = canvas

    def plot(self, data):
        self.data = data
        self.figure_controller()
        self.figure_drawer()

    #put all of your normal matplotlib stuff in here
    def figure_controller(self):
        #first run....
        if self.figure is None:
            self.figure = plt.figure()
            self.axes = self.figure.add_subplot(111)
            self.line, = self.axes.plot(self.data)
            self.axes.set_title("Example of a Matplotlib plot updating in PySimpleGUI")
        #all other runs
        else:            
            self.line.set_ydata(self.data)#update data            
            self.axes.relim() #scale the y scale
            self.axes.autoscale_view() #scale the y scale

    #finally draw the figure on a canvas
    def figure_drawer(self):
        if self.fig_agg is not None: self.fig_agg.get_tk_widget().forget()
        self.fig_agg = FigureCanvasTkAgg(self.figure, self.canvas.TKCanvas)
        self.fig_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
        self.fig_agg.draw()
