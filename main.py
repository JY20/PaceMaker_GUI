import PySimpleGUI as sg
import csv
import hashlib

from User import User

users = {}
logging = False
state = "login"
mode = ["AOOR", "AAIR", "VOOR", "VVIR"]
curMode = "none"
infoMessage = ""
dataBaseFile = "database.csv"
curUser = ""
parameterNames = ['Lower Rate Limit', 'Upper Rate Limit', 'Maximum Sensor Rate', 'Activity Threshold', 'Reaction Time', 'Response Factor', 'Recovery Time',
                  'Atrial Amplitude', 'Atrial Pulse Width', 'Ventricular Amplitude', 'Ventricular Pulse Width',
                  'Atrial Sensitivity', 'ARP', 'PVARP', 'Ventricular Sensitivity', 'VRP'
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
    f = open(dataBaseFile, "a")
    value = name+","+hashlib.sha256(password.encode('utf-8')).hexdigest()
    for i in range(len(parameterNames)):
        value += ", "
    value = value+"\n"
    f.write(value)
    if (logging):
        print("creating user: "+str(value))
    f.close()


def getAllUsers():
    f = open(dataBaseFile, "r")
    entry = f.read()
    if (entry != ""):
        user_list = entry.split("\n")
        for user in user_list:
            if (user != ""):
                values = user.split(",")
                user_parameters = {}
                for i in range(len(parameterNames)):
                    user_parameters[parameterNames[i]
                                    ] = convertStrToInt(getRealValue(values[i+2]))
                users[getRealValue(
                    values[0])] = User(getRealValue(
                        values[0]), getRealValue(
                        values[1]), user_parameters)
                if (logging):
                    print("user: "+str(values))
                    print("user: "+str(user_parameters))
    f.close()


def convertStrToInt(value):
    if(value == ""):
        return 0
    return int(value)


def getUpdatedParameters(values):
    count = 0
    updated_parameters = {}
    for parameter in parameterNamesCommon:
        updated_parameters[parameter] = convertStrToInt(
            getRealValue(values[count]))
        count += 1
    if("A" in curMode):
        for parameter in parameterNamesA:
            updated_parameters[parameter] = convertStrToInt(
                getRealValue(values[count]))
            count += 1
    if("V" in curMode):
        for parameter in parameterNamesV:
            updated_parameters[parameter] = convertStrToInt(
                getRealValue(values[count]))
            count += 1
    if("AIR" in curMode):
        for parameter in parameterNamesAIR:
            updated_parameters[parameter] = convertStrToInt(
                getRealValue(values[count]))
            count += 1
    if("VIR" in curMode):
        for parameter in parameterNamesVIR:
            updated_parameters[parameter] = convertStrToInt(
                getRealValue(values[count]))
            count += 1

    if(True):
        print("For user: "+str(curUser)+" updating "+str(updated_parameters))
    return updated_parameters


def getWindowByState():
    sizeText = 10
    sizeInput = 30
    layoutLogin = [[sg.Text(infoMessage), sg.Text()],
                   [sg.Text('Name', size=(sizeText, 1)),
                    sg.InputText(size=(sizeInput, 1))],
                   [sg.Text('Password', size=(sizeText, 1)),
                    sg.InputText(password_char='*', size=(sizeInput, 1))],
                   [sg.Text(''), sg.Text()],
                   [sg.Button('Login'), sg.Button('Create New User')]]

    sizeText = 20
    layoutCreateUser = [
        [sg.Text(infoMessage), sg.Text()],
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
        [sg.Text(infoMessage, size=(50, 3)), sg.Text()],
        [sg.Text("Mode", size=(sizeText, 1)), sg.Combo(mode, size=(
            sizeText, 1), enable_events=True)],
        [sg.Text('', size=(sizeText, 1)), sg.Text()],
    ]

    sizeText = 20
    LowerRateLimitRange = [i for i in range(30, 50, 5)] + [i for i in range(50, 90)] + [i for i in range(90, 176, 5)]
    UpperRateLimitRange = [i for i in range(50, 176, 5)]
    MaxSensorRateRange = [i for i in range(50, 176, 5)]
    ActivityThresholdRange = ['V-Low', 'Low', 'Med-Low', 'Med', 'Med-High', 'High', 'V-High']
    ReactionTimeRange = [i for i in range(10, 51, 10)]
    ResponseFactorRange = [i for i in range(1,17)]
    RecoveryTimeRange = [i for i in range(2,17)]

    layoutCommonParameters = [
        [sg.Text('Lower Rate Limit', size=(sizeText, 1)),
         sg.Spin(LowerRateLimitRange, initial_value = 60, readonly = True,  size = sizeText)],
        [sg.Text('Upper Rate Limit', size=(sizeText, 1)),
         sg.Spin(UpperRateLimitRange, initial_value = 120, readonly = True,  size = sizeText)],
        [sg.Text('Maximum Sensor Rate', size=(sizeText, 1)),
         sg.Spin(MaxSensorRateRange, initial_value = 120, readonly = True,  size = sizeText)],
        [sg.Text('Activity Threshold', size=(sizeText, 1)),
         sg.Spin(ActivityThresholdRange, initial_value = 'Med', readonly = True,  size = sizeText)],
        [sg.Text('Reaction Time', size=(sizeText, 1)),
         sg.Spin(ReactionTimeRange, initial_value = 30, readonly = True,  size = sizeText)],
        [sg.Text('Response Factor', size=(sizeText, 1)),
         sg.Spin(ResponseFactorRange, initial_value = 8, readonly = True,  size = sizeText)],
        [sg.Text('Recovery Time', size=(sizeText, 1)),
         sg.Spin(RecoveryTimeRange, initial_value = 5, readonly = True,  size = sizeText)],
    ]
    layoutA = [
        [sg.Text('Atrial Amplitude', size=(sizeText, 1)),
         sg.Spin(values=1, readonly=False,  size=sizeText)],
        [sg.Text('Atrial Pulse Width', size=(sizeText, 1)),
         sg.Spin(values=1, readonly=False,  size=sizeText)],
    ]
    layoutV = [
        [sg.Text('Ventricular Amplitude', size=(sizeText, 1)),
         sg.Spin(values=1, readonly=False,  size=sizeText)],
        [sg.Text('Ventricular Pulse Width', size=(sizeText, 1)),
         sg.Spin(values=1, readonly=False,  size=sizeText)],
    ]
    layoutAIR = [
        [sg.Text('Atrial Sensitivity', size=(sizeText, 1)),
         sg.Spin(values=1, readonly=False,  size=sizeText)],
        [sg.Text('ARP', size=(sizeText, 1)), sg.Spin(
            values=1, readonly=False,  size=sizeText)],
        [sg.Text('PVARP', size=(sizeText, 1)), sg.Spin(
            values=1, readonly=False,  size=sizeText)],
        [sg.Text('Hysteresis', size=(sizeText, 1)),
         sg.Spin(values=1, readonly=False,  size=sizeText)],
        [sg.Text('Rate Smoothing', size=(sizeText, 1)),
         sg.Spin(values=1, readonly=False,  size=sizeText)],
    ]
    layoutVIR = [
        [sg.Text('Ventricular Sensitivity', size=(sizeText, 1)),
         sg.Spin(values=1, readonly=False,  size=sizeText)],
        [sg.Text('VRP', size=(sizeText, 1)), sg.Spin(
            values=1, readonly=False,  size=sizeText)],
        [sg.Text('Hysteresis', size=(sizeText, 1)),
         sg.Spin(values=1, readonly=False,  size=sizeText)],
        [sg.Text('Rate Smoothing', size=(sizeText, 1)),
         sg.Spin(values=1, readonly=False,  size=sizeText)],
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
        if (event == 0):
            window = sg.Window('PaceMaker', layoutAOOR, resizable=True)
            curMode = "AOOR"
        elif (event == 1):
            window = sg.Window('PaceMaker', layoutAAIR, resizable=True)
            curMode = "AAIR"
        elif (event == 2):
            window = sg.Window('PaceMaker', layoutVOOR, resizable=True)
            curMode = "VOOR"
        elif (event == 3):
            window = sg.Window('PaceMaker', layoutVVIR, resizable=True)
            curMode = "VVIR"
        else:
            window = sg.Window('PaceMaker', layoutCommon, resizable=True)
            curMode = "none"
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
                    infoMessage = "User successfully created"
                    createUserDB(getRealValue(
                        values[0]), getRealValue(values[1]))
                    state = "login"
            elif (event == "Back to Login"):
                state = "login"
        elif (state == "control"):
            if (logging):
                print(event)
            if (event == "Submit Parameters"):
                print(values)
                getUpdatedParameters(values)
                infoMessage = "Parameters Successfully Updated!"
            if (event == "Log Off"):
                state = "login"
                infoMessage = "Successful log off"
        window.close()
    window.close()
