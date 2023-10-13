import PySimpleGUI as sg
import numpy as np
import json
import hashlib

from User import User
from parameterUtility import parameterUtility

maxUsers = 10  # max users

users = {}  # user dict
logging = False  # logging for print statement for debugging
state = "login"  # state of GUI
curMode = ""  # mode for the user
windowMode = "none"  # mode from events of the winodw GUI
infoMessage = ""  # info message for users
dataBaseFile = "./database/database.json"  # name and path to database
curUser = ""  # current user name
parameterUtil = parameterUtility()  # utility class object for parameter functions
mode = ["AOOR", "AAIR", "VOOR", "VVIR"]  # list of modes

# remove the spaces and get the real value


def getRealValue(value):
    return value.replace(" ", "").replace("\n", "")

# create the user in database


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
        for parameter in parameterUtil.getParameterNames():
            valueParameters[parameter] = parameterUtil.getParameterNominals()[
                parameter]
        value["parameters"] = valueParameters
        users[name] = User(value["name"], value["password"],
                           valueParameters, value["mode"])
        if (logging):
            print("creating user: "+str(value))
        updateDatabase()
        return True
    else:
        return False

# get all the json values of current users


def getAllUsersCurrentJson():
    value = {}
    for user in users:
        value[user] = users[user].getJson()
    return value

# get all users in database


def getAllUsers():
    f = open(dataBaseFile, "r")
    data = json.load(f)
    for user in data:
        users[user] = User(data[user]['name'], data[user]
                           ['password'], data[user]['parameters'], data[user]['mode'])
    f.close()

# update the database with all the users information


def updateDatabase():
    f = open(dataBaseFile, "w")
    f.write(json.dumps(getAllUsersCurrentJson(), indent=3))
    f.close()


# convert event values to parameters dicts
def getUpdatedParameters(values):
    parameterNamesCommon = ['Lower Rate Limit', 'Upper Rate Limit', 'Maximum Sensor Rate',
                            'Activity Threshold', 'Reaction Time', 'Response Factor', 'Recovery Time']
    parameterNamesA = ['Atrial Amplitude', 'Atrial Pulse Width']
    parameterNamesV = ['Ventricular Amplitude', 'Ventricular Pulse Width']
    parameterNamesAIR = ['Atrial Sensitivity', 'ARP',
                         'PVARP', 'Hysteresis', 'Rate Smoothing']
    parameterNamesVIR = ['Ventricular Sensitivity',
                         'VRP', 'Hysteresis', 'Rate Smoothing']
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


# get the window layout by state
def getWindowByState():
    connection = [('\u2B24' + ' Disconnect', 'red'),
                  ('\u2B24' + ' Connect', 'green')]
    device = [('\u2B24' + ' Different Device Approached', 'yellow'),
              ('\u2B24' + ' Same Device Approached', 'green')]
    connection_state = 0
    device_state = 1
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

    sizeText = 30
    sizeText2 = 15
    if (state == "control"):
        layoutHeader = [
            [sg.Text(infoMessage, size=(50, 3),  text_color='red'), sg.Text()],
            [sg.Text(device[device_state][0], size=(sizeText, 1), text_color=device[device_state][1]), sg.Text(connection[connection_state][0], size=(sizeText2, 1),
                                                                                                               text_color=connection[connection_state][1])],
            [sg.Text('Current Mode', size=(sizeText, 1)),
             sg.Text(curMode, size=(sizeText2, 1))],
            [sg.Text("Mode", size=(sizeText, 1)), sg.Combo(mode, size=(
                sizeText2, 1), enable_events=True, key='mode')],
            [sg.Text('', size=(sizeText, 1)), sg.Text()],
        ]
        parameters = users[curUser].getParameters()
        parameterValues = parameterUtil.getParameterRangeValues()
        layoutCommonParameters = [
            [sg.Text('Lower Rate Limit (ppm)', size=(sizeText, 1)),
             sg.Spin(parameterValues['Lower Rate Limit'], initial_value=parameters['Lower Rate Limit'], readonly=False,  size=sizeText2)],
            [sg.Text('Upper Rate Limit (ppm)', size=(sizeText, 1)),
             sg.Spin(values=parameterValues['Upper Rate Limit'], initial_value=parameters['Upper Rate Limit'], readonly=False,  size=sizeText2)],
            [sg.Text('Maximum Sensor Rate (ppm)', size=(sizeText, 1)),
             sg.Spin(values=parameterValues['Maximum Sensor Rate'], initial_value=parameters['Maximum Sensor Rate'], readonly=False,  size=sizeText2)],
            [sg.Text('Activity Threshold', size=(sizeText, 1)),
             sg.Spin(values=parameterValues['Activity Threshold'], initial_value=parameters['Activity Threshold'], readonly=False,  size=sizeText2)],
            [sg.Text('Reaction Time (sec)', size=(sizeText, 1)),
             sg.Spin(values=parameterValues['Reaction Time'], initial_value=parameters['Reaction Time'], readonly=False,  size=sizeText2)],
            [sg.Text('Response Factor', size=(sizeText, 1)),
             sg.Spin(values=parameterValues['Response Factor'], initial_value=parameters['Response Factor'], readonly=False,  size=sizeText2)],
            [sg.Text('Recovery Time (min)', size=(sizeText, 1)),
             sg.Spin(values=parameterValues['Recovery Time'], initial_value=parameters['Recovery Time'], readonly=False,  size=sizeText2)],
        ]
        layoutA = [
            [sg.Text('Atrial Amplitude', size=(sizeText, 1)),
             sg.Spin(values=parameterValues['Atrial Amplitude'], initial_value=parameters['Atrial Amplitude'], readonly=False,  size=sizeText2)],
            [sg.Text('Atrial Pulse Width (ms)', size=(sizeText, 1)),
             sg.Spin(values=parameterValues['Atrial Pulse Width'], initial_value=parameters['Atrial Pulse Width'], readonly=False,  size=sizeText2)],
        ]
        layoutV = [
            [sg.Text('Ventricular Amplitude', size=(sizeText, 1)),
             sg.Spin(values=parameterValues['Ventricular Amplitude'], initial_value=parameters['Ventricular Amplitude'], readonly=False,  size=sizeText2)],
            [sg.Text('Ventricular Pulse Width (ms)', size=(sizeText, 1)),
             sg.Spin(values=parameterValues['Ventricular Pulse Width'], initial_value=parameters['Ventricular Pulse Width'], readonly=False,  size=sizeText2)],
        ]
        layoutAIR = [
            [sg.Text('Atrial Sensitivity (mV)', size=(sizeText, 1)),
             sg.Spin(values=parameterValues['Atrial Sensitivity'], initial_value=parameters['Atrial Sensitivity'], readonly=False,  size=sizeText2)],
            [sg.Text('ARP (ms)', size=(sizeText, 1)), sg.Spin(
                values=parameterValues['ARP'], initial_value=parameters['ARP'], readonly=False,  size=sizeText2)],
            [sg.Text('PVARP (ms)', size=(sizeText, 1)), sg.Spin(
                values=parameterValues['PVARP'], initial_value=parameters['PVARP'], readonly=False,  size=sizeText2)],
            [sg.Text('Hysteresis (ppm)', size=(sizeText, 1)),
             sg.Spin(values=parameterValues['Hysteresis'], initial_value=parameters['Hysteresis'], readonly=False,  size=sizeText2)],
            [sg.Text('Rate Smoothing (%)', size=(sizeText, 1)),
             sg.Spin(values=parameterValues['Rate Smoothing'], initial_value=parameters['Rate Smoothing'], readonly=False,  size=sizeText2)],
        ]
        layoutVIR = [
            [sg.Text('Ventricular Sensitivity (mV)', size=(sizeText, 1)),
             sg.Spin(values=parameterValues['Ventricular Sensitivity'], initial_value=parameters['Ventricular Sensitivity'], readonly=False,  size=sizeText2)],
            [sg.Text('VRP (ms)', size=(sizeText, 1)), sg.Spin(
                values=parameterValues['VRP'], initial_value=parameters['VRP'], readonly=False,  size=sizeText2)],
            [sg.Text('Hysteresis (ppm)', size=(sizeText, 1)),
             sg.Spin(values=parameterValues['Hysteresis'], initial_value=parameters['Hysteresis'], readonly=False,  size=sizeText2)],
            [sg.Text('Rate Smoothing (%)', size=(sizeText, 1)),
             sg.Spin(values=parameterValues['Rate Smoothing'], initial_value=parameters['Rate Smoothing'], readonly=False,  size=sizeText2)],
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


# main function to run GUI
if __name__ == '__main__':
    try:
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
                        curMode = users[getRealValue(values[0])].getMode()
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
                    newParameters = getUpdatedParameters(values)
                    check = parameterUtil.checkParameterInRange(newParameters)
                    if(check == None):
                        users[curUser].updateParameters(newParameters)
                        users[curUser].setMode(curMode)
                        infoMessage = "Parameters Successfully Updated!"
                        updateDatabase()
                        getAllUsers()
                    else:
                        infoMessage = "Double check the value entered are in range for parameter: " + \
                            str(check)
                if (event == "Log Off"):
                    state = "login"
                    infoMessage = "Successful log off"
            window.close()
        window.close()
    except Exception as e:
        window.close()
        sg.popup_error_with_traceback(
            "An error had occured. Please contact the support team with the following info: ", e)