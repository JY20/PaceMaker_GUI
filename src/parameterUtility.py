import numpy as np


class parameterUtility:
    # constructor for all range values for parameters, parameter names, and parameter nominals
    def __init__(self):
        self.parameterNames = ['Lower Rate Limit', 'Upper Rate Limit', 'Maximum Sensor Rate', 'Activity Threshold', 'Reaction Time', 'Response Factor', 'Recovery Time',
                               'Atrial Amplitude', 'Atrial Pulse Width', 'Ventricular Amplitude', 'Ventricular Pulse Width',
                               'Atrial Sensitivity', 'ARP', 'PVARP', 'Ventricular Sensitivity', 'VRP',
                               'Hysteresis', 'Rate Smoothing']
        parameterUpperLimit = {'Lower Rate Limit': 2000, 'Upper Rate Limit': 175, 'Maximum Sensor Rate': 175, 'Activity Threshold': 2000, 'Reaction Time': 50, 'Response Factor': 16, 'Recovery Time': 16,
                               'Atrial Amplitude':  5000, 'Atrial Pulse Width': 1.9, 'Ventricular Amplitude': 5000, 'Ventricular Pulse Width': 1.9,
                               'Atrial Sensitivity': 10, 'ARP': 500, 'PVARP': 500, 'Ventricular Sensitivity': 10, 'VRP': 500,
                               'Hysteresis': 3000, 'Rate Smoothing': 3000}
        parameterLowerLimit = {'Lower Rate Limit': 200, 'Upper Rate Limit': 50, 'Maximum Sensor Rate': 50, 'Activity Threshold': 200, 'Reaction Time': 10, 'Response Factor': 1, 'Recovery Time': 2,
                               'Atrial Amplitude':  500, 'Atrial Pulse Width': 0.01, 'Ventricular Amplitude': 500, 'Ventricular Pulse Width': 0.01,
                               'Atrial Sensitivity': 1, 'ARP': 150, 'PVARP': 150, 'Ventricular Sensitivity': 1, 'VRP': 150,
                               'Hysteresis': 300, 'Rate Smoothing': 300}

        parameterIncrements = {'Lower Rate Limit': 2, 'Upper Rate Limit': 5, 'Maximum Sensor Rate': 5, 'Activity Threshold': 2, 'Reaction Time': 10, 'Response Factor': 1, 'Recovery Time': 1,
                               'Atrial Amplitude':  2, 'Atrial Pulse Width': 0.01, 'Ventricular Amplitude': 5, 'Ventricular Pulse Width': 0.01,
                               'Atrial Sensitivity': 0.5, 'ARP': 10, 'PVARP': 10, 'Ventricular Sensitivity': 0.5, 'VRP': 10,
                               'Hysteresis': 2, 'Rate Smoothing': 3}
        self.parameterValues = {}
        for parameter in self.parameterNames:
            if(parameter == 'Lower Rate Limit'):
                self.parameterValues[parameter] = [i for i in np.arange(
                    30, 50+5, 5)] + [i for i in np.arange(50, 90+1, 1)] + [i for i in np.arange(90, 175+5, 5)]
                self.parameterValues[parameter] = np.round(
                    self.parameterValues[parameter], 2)
            elif(parameter == 'Hysteresis'):
                self.parameterValues[parameter] = [0]+[i for i in np.arange(
                    30, 50+5, 5)] + [i for i in np.arange(50, 90+1, 1)] + [i for i in np.arange(90, 175+5, 5)]
                self.parameterValues[parameter] = np.round(
                    self.parameterValues[parameter], 2)
            elif(parameter == 'Activity Threshold'):
                self.parameterValues[parameter] = ['V-Low', 'Low',
                                                   'Med-Low', 'Med', 'Med-High', 'High', 'V-High']
            elif(parameter == 'Rate Smoothing'):
                self.parameterValues[parameter] = [
                    0, 3, 6, 9, 12, 15, 18, 21, 25]
            elif(parameter == 'Atrial Sensitivity' or parameter == 'Ventricular Sensitivity'):
                self.parameterValues[parameter] = [0.25, 0.5, 0.75] + [i for i in np.arange(
                    parameterLowerLimit[parameter], parameterUpperLimit[parameter]+parameterIncrements[parameter], parameterIncrements[parameter])]
                self.parameterValues[parameter] = np.round(
                    self.parameterValues[parameter], 2)
            elif(parameter == 'Atrial Pulse Width' or parameter == 'Ventricular Pulse Width'):
                self.parameterValues[parameter] = [0.05]+[i for i in np.arange(
                    parameterLowerLimit[parameter], parameterUpperLimit[parameter]+parameterIncrements[parameter], parameterIncrements[parameter])]
                self.parameterValues[parameter] = np.round(
                    self.parameterValues[parameter], 2)
            elif(parameter == 'Atrial Amplitude' or parameter == 'Ventricular Amplitude'):
                self.parameterValues[parameter] = [
                    0] + [i for i in np.arange(0.5, 3.2+0.1, 0.1)] + [i for i in np.arange(3.5, 7+0.5, 0.5)]
                self.parameterValues[parameter] = np.round(
                    self.parameterValues[parameter], 2)
            else:
                self.parameterValues[parameter] = [i for i in np.arange(
                    parameterLowerLimit[parameter], parameterUpperLimit[parameter]+parameterIncrements[parameter], parameterIncrements[parameter])]
                self.parameterValues[parameter] = np.round(
                    self.parameterValues[parameter], 2)
        self.parameterNominals = {'Lower Rate Limit': 60, 'Upper Rate Limit': 120, 'Maximum Sensor Rate': 120, 'Activity Threshold': 'Med', 'Reaction Time': 30, 'Response Factor': 8, 'Recovery Time': 5,
                                  'Atrial Amplitude':  3.5, 'Atrial Pulse Width': 0.4, 'Ventricular Amplitude': 3.5, 'Ventricular Pulse Width': 0.4,
                                  'Atrial Sensitivity': 0.75, 'ARP': 250, 'PVARP': 250, 'Ventricular Sensitivity': 2.5, 'VRP': 250,
                                  'Hysteresis': 0, 'Rate Smoothing': 0}

    # get the parameter range values
    def getParameterRangeValues(self):
        return self.parameterValues
    # get the parameter names

    def getParameterNames(self):
        return self.parameterNames
    # get the parameter nominals

    def getParameterNominals(self):
        return self.parameterNominals

    # checks if parameter value is in range
    def checkParameterInRange(self, newParameterValues):
        for parameter in newParameterValues:
            if(type(newParameterValues[parameter]) == str):
                newParameterValues[parameter] = np.float64(
                    newParameterValues[parameter])
            if(newParameterValues[parameter] not in self.parameterValues[parameter]):
                return parameter
        return None
