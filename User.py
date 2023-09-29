import hashlib


class User:
    def __init__(self, name, password, parameters):
        self.name = name
        self.password = password
        self.parameters = parameters

    def checkCredential(self, name, password):
        if(self.name == name and hashlib.sha256(password.encode('utf-8')).hexdigest() == self.password):
            return True
        else:
            return False

    def getParameters(self):
        return self.parameters.copy()

    def updateParameters(self, newParameters):
        for parameter in newParameters:
            self.parameters[parameter] = newParameters[parameter]

    def valuesToStr(self):
        parameterNames = ['Lower Rate Limit', 'Upper Rate Limit', 'Maximum Sensor Rate', 'Activity Threshold', 'Reaction Time', 'Response Factor', 'Recovery Time',
                          'Atrial Amplitude', 'Atrial Pulse Width', 'Ventricular Amplitude', 'Ventricular Pulse Width',
                          'Atrial Sensitivity', 'ARP', 'PVARP', 'Ventricular Sensitivity', 'VRP',
                          'Hysteresis', 'Rate Smoothing']
        strValue = self.name+"," + self.password
        for parameter in parameterNames:
            strValue += ","+str(self.parameters[parameter])
        strValue = strValue+"\n"
        return strValue
