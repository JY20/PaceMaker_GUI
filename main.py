import PySimpleGUI as sg
import numpy as np
import json
import hashlib

from User import User

maxUsers = 10

users = {}
logging = False
state = "login"
mode = ["AOOR", "AAIR", "VOOR", "VVIR"]
curMode = ""
windowMode = "none"
infoMessage = ""
dataBaseFile = "database.json"
curUser = ""
parameterNames = ['Lower Rate Limit', 'Upper Rate Limit', 'Maximum Sensor Rate', 'Activity Threshold', 'Reaction Time', 'Response Factor', 'Recovery Time',
                  'Atrial Amplitude', 'Atrial Pulse Width', 'Ventricular Amplitude', 'Ventricular Pulse Width',
                  'Atrial Sensitivity', 'ARP', 'PVARP', 'Ventricular Sensitivity', 'VRP',
                  'Hysteresis', 'Rate Smoothing']

parameterNamesCommon = ['Lower Rate Limit', 'Upper Rate Limit', 'Maximum Sensor Rate',
                        'Activity Threshold', 'Reaction Time', 'Response Factor', 'Recovery Time']
parameterNamesA = ['Atrial Amplitude', 'Atrial Pulse Width']
parameterNamesV = ['Ventricular Amplitude', 'Ventricular Pulse Width']
parameterNamesAIR = ['Atrial Sensitivity', 'ARP',
                     'PVARP', 'Hysteresis', 'Rate Smoothing']
parameterNamesVIR = ['Ventricular Sensitivity',
                     'VRP', 'Hysteresis', 'Rate Smoothing']


def getRealValue(value):
    return value.replace(" ", "").replace("\n", "")


def createUserDB(name, password):
    if(logging):
        print(str(len(users)+1)+"/"+str(maxUsers))
    if(len(users)+1 <= maxUsers):
        value = {}
        value["name"] = name
        value["password"] = hashlib.sha256(
            password.encode('utf-8')).hexdigest()
        value["mode"] = "none"
        valueParameters = {}
        for parameter in parameterNames:
            valueParameters[parameter] = None
        value["parameters"] = valueParameters
        users[name] = User(value["name"], value["password"],
                           valueParameters, value["mode"])
        if (logging):
            print("creating user: "+str(value))
        updateDatabase()
        return True
    else:
        return False


def getAllUsersCurrentJson():
    value = {}
    for user in users:
        value[user] = users[user].getJson()
    return value


def getAllUsers():
    f = open(dataBaseFile, "r")
    data = json.load(f)
    for user in data:
        users[user] = User(data[user]['name'], data[user]
                           ['password'], data[user]['parameters'], data[user]['mode'])
    f.close()


def updateDatabase():
    f = open(dataBaseFile, "w")
    f.write(json.dumps(getAllUsersCurrentJson(), indent=3))
    f.close()


def convertStrToInt(value):
    if(value == ""):
        return 0
    return int(value)


def getUpdatedParameters(values):
    count = 0
    updated_parameters = {}
    for parameter in parameterNamesCommon:
        updated_parameters[parameter] = values[count]
        count += 1
    if("A" in curMode):
        for parameter in parameterNamesA:
            updated_parameters[parameter] = values[count]
            count += 1
    if("V" in curMode):
        for parameter in parameterNamesV:
            updated_parameters[parameter] = values[count]
            count += 1
    if("AIR" in curMode):
        for parameter in parameterNamesAIR:
            updated_parameters[parameter] = values[count]
            count += 1
    if("VIR" in curMode):
        for parameter in parameterNamesVIR:
            updated_parameters[parameter] = values[count]
            count += 1

    if(logging):
        print("For user: "+str(curUser)+" updating "+str(updated_parameters))
    return updated_parameters


def getWindowByState():
    sizeText = 10
    sizeInput = 30
    layoutLogin = [[sg.Text(infoMessage, text_color='red'), sg.Text()],
                   [sg.Text('Name', size=(sizeText, 1)),
                    sg.InputText(size=(sizeInput, 1))],
                   [sg.Text('Password', size=(sizeText, 1)),
                    sg.InputText(password_char='*', size=(sizeInput, 1))],
                   [sg.Text(''), sg.Text()],
                   [sg.Button('Login'), sg.Button('Create New User')]]

    sizeText = 20
    layoutCreateUser = [
        [sg.Text(infoMessage, text_color='red'), sg.Text()],
        [sg.Text('Name', size=(sizeText, 1)),
         sg.InputText(size=(sizeInput, 1))],
        [sg.Text('Password', size=(sizeText, 1)),
         sg.InputText(password_char='*', size=(sizeInput, 1))],
        [sg.Text('Confirm Password', size=(sizeText, 1)),
         sg.InputText(password_char='*', size=(sizeInput, 1))],
        [sg.Text('', size=(sizeText, 1)), sg.Text()],
        [sg.Button('Create New User')], [sg.Button('Back to Login')]]

    sizeText = 20
    layoutHeader = [
        [sg.Text(infoMessage, size=(50, 3),  text_color='red'), sg.Text()],
        [sg.Text("Mode", size=(sizeText, 1)), sg.Combo(mode, size=(
            sizeText, 1), enable_events=True, key='mode')],
        [sg.Text('', size=(sizeText, 1)), sg.Text()],
    ]

    sizeText = 20
    if (state == "control"):
        parameters = users[curUser].getParameters()
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

        parameterValues = {}
        for parameter in parameterNames:
            if(parameter == 'Lower Rate Limit' or parameter == 'Hysteresis'):
                parameterValues[parameter] = [i for i in np.arange(
                    30, 50+5, 5)] + [i for i in np.arange(50, 90+1, 1)] + [i for i in np.arange(90, 175+5, 5)]
            elif(parameter == 'Activity Threshold'):
                parameterValues[parameter] = ['V-Low', 'Low',
                                              'Med-Low', 'Med', 'Med-High', 'High', 'V-High']
            elif(parameter == 'Rate Smoothing'):
                parameterValues[parameter] = [0, 3, 6, 9, 12, 15, 18, 21, 25]
            elif(parameter == 'Atrial Sensitivity' or parameter == 'Ventricular Sensitivity'):
                parameterValues[parameter] = [0.25, 0.5, 0.75] + [i for i in np.arange(
                    parameterLowerLimit[parameter], parameterUpperLimit[parameter]+parameterIncrements[parameter], parameterIncrements[parameter])]
            elif(parameter == 'Atrial Pulse Width' or parameter == 'Ventricular Pulse Width'):
                parameterValues[parameter] = [0.05]+[i for i in np.arange(
                    parameterLowerLimit[parameter], parameterUpperLimit[parameter]+parameterIncrements[parameter], parameterIncrements[parameter])]
            if(parameter == 'Atrial Amplitude' or parameter == 'Ventricular Amplitude'):
                parameterValues[parameter] = [
                    0] + [i for i in np.arange(0.5, 3.2+0.1, 0.1)] + [i for i in np.arange(3.5, 7, 0.5)]
            else:
                parameterValues[parameter] = [i for i in np.arange(
                    parameterLowerLimit[parameter], parameterUpperLimit[parameter]+parameterIncrements[parameter], parameterIncrements[parameter])]

        layoutCommonParameters = [
            [sg.Text('Lower Rate Limit (ppm)', size=(sizeText, 1)),
             sg.Spin(parameterValues['Lower Rate Limit'], initial_value=parameters['Lower Rate Limit'], readonly=False,  size=sizeText)],
            [sg.Text('Upper Rate Limit (ppm)', size=(sizeText, 1)),
             sg.Spin(values=parameterValues['Upper Rate Limit'], initial_value=parameters['Upper Rate Limit'], readonly=False,  size=sizeText)],
            [sg.Text('Maximum Sensor Rate (ppm)', size=(sizeText, 1)),
             sg.Spin(values=parameterValues['Maximum Sensor Rate'], initial_value=parameters['Maximum Sensor Rate'], readonly=False,  size=sizeText)],
            [sg.Text('Activity Threshold', size=(sizeText, 1)),
             sg.Spin(values=parameterValues['Activity Threshold'], initial_value=parameters['Activity Threshold'], readonly=False,  size=sizeText)],
            [sg.Text('Reaction Time (sec)', size=(sizeText, 1)),
             sg.Spin(values=parameterValues['Reaction Time'], initial_value=parameters['Reaction Time'], readonly=False,  size=sizeText)],
            [sg.Text('Response Factor', size=(sizeText, 1)),
             sg.Spin(values=parameterValues['Response Factor'], initial_value=parameters['Response Factor'], readonly=False,  size=sizeText)],
            [sg.Text('Recovery Time (min)', size=(sizeText, 1)),
             sg.Spin(values=parameterValues['Recovery Time'], initial_value=parameters['Recovery Time'], readonly=False,  size=sizeText)],
        ]
        layoutA = [
            [sg.Text('Atrial Amplitude', size=(sizeText, 1)),
             sg.Spin(values=parameterValues['Atrial Amplitude'], initial_value=parameters['Atrial Amplitude'], readonly=False,  size=sizeText)],
            [sg.Text('Atrial Pulse Width (ms)', size=(sizeText, 1)),
             sg.Spin(values=parameterValues['Atrial Pulse Width'], initial_value=parameters['Atrial Pulse Width'], readonly=False,  size=sizeText)],
        ]
        layoutV = [
            [sg.Text('Ventricular Amplitude', size=(sizeText, 1)),
             sg.Spin(values=parameterValues['Ventricular Amplitude'], initial_value=parameters['Ventricular Amplitude'], readonly=False,  size=sizeText)],
            [sg.Text('Ventricular Pulse Width (ms)', size=(sizeText, 1)),
             sg.Spin(values=parameterValues['Ventricular Pulse Width'], initial_value=parameters['Ventricular Pulse Width'], readonly=False,  size=sizeText)],
        ]
        layoutAIR = [
            [sg.Text('Atrial Sensitivity (mV)', size=(sizeText, 1)),
             sg.Spin(values=parameterValues['Atrial Sensitivity'], initial_value=parameters['Atrial Sensitivity'], readonly=False,  size=sizeText)],
            [sg.Text('ARP (ms)', size=(sizeText, 1)), sg.Spin(
                values=parameterValues['ARP'], initial_value=parameters['ARP'], readonly=False,  size=sizeText)],
            [sg.Text('PVARP (ms)', size=(sizeText, 1)), sg.Spin(
                values=parameterValues['PVARP'], initial_value=parameters['PVARP'], readonly=False,  size=sizeText)],
            [sg.Text('Hysteresis (ppm)', size=(sizeText, 1)),
             sg.Spin(values=parameterValues['Hysteresis'], initial_value=parameters['Hysteresis'], readonly=False,  size=sizeText)],
            [sg.Text('Rate Smoothing (%)', size=(sizeText, 1)),
             sg.Spin(values=parameterValues['Rate Smoothing'], initial_value=parameters['Rate Smoothing'], readonly=False,  size=sizeText)],
        ]
        layoutVIR = [
            [sg.Text('Ventricular Sensitivity (mV)', size=(sizeText, 1)),
             sg.Spin(values=parameterValues['Ventricular Sensitivity'], initial_value=parameters['Ventricular Sensitivity'], readonly=False,  size=sizeText)],
            [sg.Text('VRP (ms)', size=(sizeText, 1)), sg.Spin(
                values=parameterValues['VRP'], initial_value=parameters['VRP'], readonly=False,  size=sizeText)],
            [sg.Text('Hysteresis (ppm)', size=(sizeText, 1)),
             sg.Spin(values=parameterValues['Hysteresis'], initial_value=parameters['Hysteresis'], readonly=False,  size=sizeText)],
            [sg.Text('Rate Smoothing (%)', size=(sizeText, 1)),
             sg.Spin(values=parameterValues['Rate Smoothing'], initial_value=parameters['Rate Smoothing'], readonly=False,  size=sizeText)],
        ]
        layoutSubmit = [
            sg.Button('Submit Parameters')
        ]
        layoutLogOff = [
            sg.Button('Log Off')
        ]
        layoutCommon = [layoutHeader, layoutLogOff]
        layoutAOOR = [
            layoutHeader,
            layoutCommonParameters,
            layoutA,
            layoutSubmit,
            layoutLogOff
        ]
        layoutAAIR = [
            layoutHeader,
            layoutCommonParameters,
            layoutA,
            layoutAIR,
            layoutSubmit,
            layoutLogOff
        ]
        layoutVOOR = [
            layoutHeader,
            layoutCommonParameters,
            layoutV,
            layoutSubmit,
            layoutLogOff
        ]
        layoutVVIR = [
            layoutHeader,
            layoutCommonParameters,
            layoutV,
            layoutVIR,
            layoutSubmit,
            layoutLogOff
        ]

    if (state == "login"):
        window = sg.Window('PaceMaker', layoutLogin, resizable=True)
        return window
    elif (state == "control"):
        if(logging):
            print(event)
        if (windowMode == "AOOR"):
            window = sg.Window('PaceMaker', layoutAOOR, resizable=True)
        elif (windowMode == "AAIR"):
            window = sg.Window('PaceMaker', layoutAAIR, resizable=True)
        elif (windowMode == "VOOR"):
            window = sg.Window('PaceMaker', layoutVOOR, resizable=True)
        elif (windowMode == "VVIR"):
            window = sg.Window('PaceMaker', layoutVVIR, resizable=True)
        else:
            window = sg.Window('PaceMaker', layoutCommon, resizable=True)
        return window
    elif (state == "createUser"):
        window = sg.Window('PaceMaker', layoutCreateUser, resizable=True)
        return window


if __name__ == '__main__':
    sg.theme('LightGrey1')

    while True:
        window = getWindowByState()

        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':
            window.close()
            break

        if (logging):
            print(state)

        if (state == "login"):
            getAllUsers()
            if (event == "Login"):
                if (logging):
                    print(values)
                if (users.get(getRealValue(values[0])) and users[getRealValue(values[0])].checkCredential(getRealValue(values[0]), getRealValue(values[1]))):
                    infoMessage = ""
                    state = "control"
                    curUser = getRealValue(values[0])
                    infoMessage = "Welcome to Control Panel for: " + curUser
                    windowMode = users[getRealValue(values[0])].getMode()
                else:
                    infoMessage = "Password Incorrect or this user does not exist"
            elif (event == "Create New User"):
                infoMessage = ""
                state = "createUser"
        elif (state == "createUser"):
            if (event == "Create New User"):
                if (not (getRealValue(values[1]) == getRealValue(values[2]))):
                    infoMessage = "Password mismatch"
                elif (users.get(getRealValue(values[0]))):
                    infoMessage = "User already exists"
                else:
                    if (logging):
                        print("Creating New User: "+values[0])
                    if(createUserDB(getRealValue(
                            values[0]), getRealValue(values[1]))):
                        infoMessage = "User successfully created"
                    else:
                        infoMessage = "System had reached to max number of users. Please contact support team for help"

                    state = "login"
            elif (event == "Back to Login"):
                state = "login"
        elif (state == "control"):
            windowMode = values['mode']
            if(windowMode in mode):
                curMode = windowMode
            if (logging):
                print(event)
                print(values)
            if (event == "Submit Parameters"):
                users[curUser].updateParameters(getUpdatedParameters(values))
                users[curUser].setMode(curMode)
                infoMessage = "Parameters Successfully Updated!"
                updateDatabase()
                getAllUsers()
            if (event == "Log Off"):
                state = "login"
                infoMessage = "Successful log off"
        window.close()
    window.close()
