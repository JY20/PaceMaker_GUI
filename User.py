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

    def getName(self):
        return self.name

    def getJson(self):
        parameterNames = ['Lower Rate Limit', 'Upper Rate Limit', 'Maximum Sensor Rate', 'Activity Threshold', 'Reaction Time', 'Response Factor', 'Recovery Time',
                          'Atrial Amplitude', 'Atrial Pulse Width', 'Ventricular Amplitude', 'Ventricular Pulse Width',
                          'Atrial Sensitivity', 'ARP', 'PVARP', 'Ventricular Sensitivity', 'VRP',
                          'Hysteresis', 'Rate Smoothing']
        value = {}
        value["name"] = self.name
        value["password"] = self.password
        valueParameters = {}
        for parameter in parameterNames:
            valueParameters[parameter] = self.parameters[parameter]
        value["parameters"] = valueParameters
        return value
