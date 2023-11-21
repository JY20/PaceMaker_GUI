import numpy as np


class parameterUtility:
    # constructor for all range values for parameters, parameter names, and parameter nominals
    def __init__(self):
        self.parameterNames = ['Lower Rate Limit', 'Upper Rate Limit', 'Maximum Sensor Rate', 'Activity Threshold', 'Reaction Time', 'Response Factor', 'Recovery Time',
                               'Atrial Amplitude', 'Atrial Pulse Width', 'Ventricular Amplitude', 'Ventricular Pulse Width',
                               'Atrial Sensitivity', 'ARP', 'PVARP', 'Ventricular Sensitivity', 'VRP',
                               'Hysteresis', 'Rate Smoothing', 'Fixed AV delay', 'Dynamic AV delay','Minimum Dynamic AV delay', 
                               'Sensed AV delay offset', 'PVARP Extension', 'ATR Mode', 'ATR Duration','ATR Fallback Time', 'Ventricular Blanking']
        parameterUpperLimit = {'Lower Rate Limit': 2000, 'Upper Rate Limit': 175, 'Maximum Sensor Rate': 175, 'Activity Threshold': 2000, 'Reaction Time': 50, 'Response Factor': 16, 'Recovery Time': 16,
                               'Atrial Amplitude':  5, 'Atrial Pulse Width': 30, 'Ventricular Amplitude': 5, 'Ventricular Pulse Width':30,
                               'Atrial Sensitivity': 5, 'ARP': 500, 'PVARP': 500, 'Ventricular Sensitivity': 5, 'VRP': 500,
                               'Hysteresis': 3000, 'Rate Smoothing': 3000, 'Fixed AV delay':300, 'Dynamic AV delay':0,'Minimum Dynamic AV delay':100, 
                               'Sensed AV delay offset':0, 'PVARP Extension':400, 'ATR Mode':0, 'ATR Duration':0,'ATR Fallback Time':5, 'Ventricular Blanking':60}
        parameterLowerLimit = {'Lower Rate Limit': 200, 'Upper Rate Limit': 50, 'Maximum Sensor Rate': 50, 'Activity Threshold': 200, 'Reaction Time': 10, 'Response Factor': 1, 'Recovery Time': 2,
                               'Atrial Amplitude':  0, 'Atrial Pulse Width': 1, 'Ventricular Amplitude': 0, 'Ventricular Pulse Width': 1,
                               'Atrial Sensitivity': 0, 'ARP': 150, 'PVARP': 150, 'Ventricular Sensitivity': 0, 'VRP': 150,
                               'Hysteresis': 300, 'Rate Smoothing': 300,'Fixed AV delay': 70, 'Dynamic AV delay':0,'Minimum Dynamic AV delay':30, 
                               'Sensed AV delay offset':-100, 'PVARP Extension':0, 'ATR Mode':0, 'ATR Duration':0,'ATR Fallback Time':1, 'Ventricular Blanking':30}

        parameterIncrements = {'Lower Rate Limit': 2, 'Upper Rate Limit': 5, 'Maximum Sensor Rate': 5, 'Activity Threshold': 2, 'Reaction Time': 10, 'Response Factor': 1, 'Recovery Time': 1,
                               'Atrial Amplitude':  0.1, 'Atrial Pulse Width': 1, 'Ventricular Amplitude': 0.1, 'Ventricular Pulse Width': 1,
                               'Atrial Sensitivity': 0.1, 'ARP': 10, 'PVARP': 10, 'Ventricular Sensitivity': 0.1, 'VRP': 10,
                               'Hysteresis': 2, 'Rate Smoothing': 3,'Fixed AV delay':10, 'Dynamic AV delay':1,'Minimum Dynamic AV delay':10, 
                               'Sensed AV delay offset':10, 'PVARP Extension':50, 'ATR Mode':1, 'ATR Duration':1,'ATR Fallback Time':1, 'Ventricular Blanking':10}
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
            elif(parameter == 'Dynamic AV delay' or parameter == 'ATR Mode'):
                self.parameterValues[parameter] = ['Off', 'On']
            elif(parameter == 'ATR Duration'):
                self.parameterValues[parameter] = [10]+[i for i in np.arange(20, 80+20,20)]+[i for i in np.arange(100, 2000,100)]
                self.parameterValues[parameter] = np.round(
                    self.parameterValues[parameter], 2)
            else:
                self.parameterValues[parameter] = [i for i in np.arange(
                    parameterLowerLimit[parameter], parameterUpperLimit[parameter]+parameterIncrements[parameter], parameterIncrements[parameter])]
                self.parameterValues[parameter] = np.round(
                    self.parameterValues[parameter], 2)
        parameterNominals = {'Lower Rate Limit': 60, 'Upper Rate Limit': 120, 'Maximum Sensor Rate': 120, 'Activity Threshold': 'Med', 'Reaction Time': 30, 'Response Factor': 8, 'Recovery Time': 5,
                                  'Atrial Amplitude':  5, 'Atrial Pulse Width': 1, 'Ventricular Amplitude': 5, 'Ventricular Pulse Width': 1,
                                  'Atrial Sensitivity': 0, 'ARP': 250, 'PVARP': 250, 'Ventricular Sensitivity': 0, 'VRP': 250,
                                  'Hysteresis': 0, 'Rate Smoothing': 0, 'Fixed AV delay': 150, 'Dynamic AV delay':'Off','Minimum Dynamic AV delay':50, 
                               'Sensed AV delay offset':0, 'PVARP Extension':0, 'ATR Mode':'Off', 'ATR Duration':20,'ATR Fallback Time':1, 'Ventricular Blanking':40}
        
        self.parameterNominals = {}
        for parameter in self.parameterNames:
            if(str(type(self.parameterValues[parameter][0])) == str(np.int32) or str(type(self.parameterValues[parameter][0])) == str(int)):
                self.parameterNominals[parameter] = int(parameterNominals[parameter])
                temp =  []
                for value in self.parameterValues[parameter]:
                    temp.append(int(value))
                self.parameterValues[parameter] = temp
            elif(str(type(self.parameterValues[parameter][0])) == str(np.float64)):
                self.parameterNominals[parameter] = float(parameterNominals[parameter])
                temp =  []
                for value in self.parameterValues[parameter]:
                    temp.append(float(value))
                self.parameterValues[parameter] = temp
            elif(str(type(self.parameterValues[parameter][0])) == str(str)):
                self.parameterNominals[parameter] = str(parameterNominals[parameter])
                temp =  []
                for value in self.parameterValues[parameter]:
                    temp.append(str(value))
                self.parameterValues[parameter] = temp

        for parameter in self.parameterValues:
            if (type(self.parameterValues[parameter]) == np.ndarray):
                self.parameterValues[parameter] = self.parameterValues[parameter].tolist()

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
            if(str(type(self.parameterValues[parameter][0])) == str(int)):
                newParameterValues[parameter] = int(newParameterValues[parameter])
            elif(str(type(self.parameterValues[parameter][0])) == str(float)):
                newParameterValues[parameter] = float(newParameterValues[parameter])
            elif(str(type(self.parameterValues[parameter][0])) == str(str)):
                newParameterValues[parameter] = str(newParameterValues[parameter])

            if(newParameterValues[parameter] not in self.parameterValues[parameter]):
                return parameter
        return None
