import numpy as np

class egramUtility:
  # constructor for egram matrix
  def __init__(self):
    self.numberOfObservations = 100
    self.egramData = {}
    # generate random voltages until we have real ones
    self.egramData["time"] = [10*i for i in range(self.numberOfObservations)]
    self.egramData["voltage"] = [np.random.random() for i in range(self.numberOfObservations)]
