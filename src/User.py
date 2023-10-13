import hashlib
import numpy as np


class User:

    # constructor for user
    def __init__(self, name, password, parameters, mode):
        self.name = name
        self.password = password
        self.parameters = parameters
        self.mode = mode

    # checks the credentials of the user
    def checkCredential(self, name, password):
        if(self.name == name and hashlib.sha256(password.encode('utf-8')).hexdigest() == self.password):
            return True
        else:
            return False

    # get user's parameter dict
    def getParameters(self):
        return self.parameters.copy()

    # update user's parameter dict
    def updateParameters(self, newParameters):
        for parameter in newParameters:
            self.parameters[parameter] = newParameters[parameter]
    # get user's name

    def getName(self):
        return self.name
    # get user's mode

    def getMode(self):
        return self.mode
    # set user's mode

    def setMode(self, mode):
        self.mode = mode

    # get json format of user variables
    def getJson(self):
        parameterNames = ['Lower Rate Limit', 'Upper Rate Limit', 'Maximum Sensor Rate', 'Activity Threshold', 'Reaction Time', 'Response Factor', 'Recovery Time',
                          'Atrial Amplitude', 'Atrial Pulse Width', 'Ventricular Amplitude', 'Ventricular Pulse Width',
                          'Atrial Sensitivity', 'ARP', 'PVARP', 'Ventricular Sensitivity', 'VRP',
                          'Hysteresis', 'Rate Smoothing']
        value = {}
        value["name"] = self.name
        value["password"] = self.password
        value["mode"] = self.mode
        valueParameters = {}
        for parameter in parameterNames:
            valueParameters[parameter] = self.parameters[parameter]
            if(type(valueParameters[parameter]) == type(np.int32(1))):
                valueParameters[parameter] = int(valueParameters[parameter])
            elif(type(valueParameters[parameter]) == type(np.float64(1))):
                valueParameters[parameter] = float(valueParameters[parameter])
        value["parameters"] = valueParameters
        return value
