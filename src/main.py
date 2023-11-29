from parameterUtility import parameterUtility
from User import User
from egramPlot import updateable_matplotlib_plot
import matplotlib.pyplot as plt
import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import matplotlib
import time
import threading
import random
import numpy as np
import json
import hashlib
import os
import matplotlib
import serial
import struct
matplotlib.use('TkAgg')

maxUsers = 10  # max users

users = {}  # user dict
logging = False  # logging for print statement for debugging
state = "login"  # state of GUI
curMode = ""  # mode for the user
windowMode = "none"  # mode from events of the winodw GUI
infoMessage = ""  # info message for users
dataBaseFile = "./database/database_dev.json"  # name and path to database
curUser = ""  # current user name
parameterUtil = parameterUtility()  # utility class object for parameter functions
mode = ["AOO", "AAI", "VOO", "VVI", "AOOR",
        "AAIR", "VOOR", "VVIR", "DDDR"]  # list of modes
# dict for atrial and ventricular list of egram data
egramData = {"vent": [], "atr": []}
tempCounter = 0
path = ""


def serialCommunicate(recieve=False):
    path = serial.Serial('COM22', 115200)
    sendValue = struct.pack("7s", curMode.encode())
    
    userParameters = users[curUser].getParameters()

    for parameter in parameterUtil.parameterNames:
        if(str(type(userParameters[parameter])) == str(int)):
            sendValue += struct.pack("h", userParameters[parameter])
        elif(str(type(userParameters[parameter])) == str(float)):
            sendValue += struct.pack("f", userParameters[parameter])
        elif(str(type(userParameters[parameter])) == str(str)):
            sendValue += struct.pack("7s", userParameters[parameter].encode())

    path.write(b'\x16') # SYNC
    if(recieve):
        path.write(b'\x55') # FN_CODE
    else:
        path.write(b'\x56')
    path.write(sendValue)

    if(recieve):
        return path



def readEgramData(path):
    data = path.readline()
    if len(data) == 17:
        print(data)

        vent_data = struct.unpack('d',data[0:8])[0]
        atr_data = struct.unpack('d',data[8:16])[0]

        print(f"v: {vent_data}\t\ta: {atr_data}")
        print(type(vent_data))
        updateEgramData(atr_data, vent_data)
        
# remove the spaces and get the real value


def getRealValue(value):
    return value.replace(" ", "").replace("\n", "")

def updateEgramData(newAtrData, newVentData):
    newAtr = egramData['atr'][1:]
    newAtr.append(newAtrData)
    egramData['atr'] = newAtr
    newVent = egramData['vent'][1:]
    newVent.append(newVentData)
    egramData['vent'] = newVent

def tempData():
    updateEgramData(random.randint(0, 100)/100, random.randint(0, 100)/100)

def defaultEgramData():
    for i in range(0, 50):
        egramData['vent'].append(0)
        egramData['atr'].append(0)

def checkValid(value):
    if (value == ""):
        return "Invalid name/password"
    elif(" " in value):
        return "Please avoid space in name/password"
    return None

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

# update the database file path when run from pacemaker_gui instead


def updateDataBaseFile():
    if("src" not in os.getcwd()):
        newdataBaseFile = "./src/"+dataBaseFile.split("./")[1]
        return newdataBaseFile
    return dataBaseFile

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
    parameterNamesCommon = ['Lower Rate Limit',
                            'Upper Rate Limit']
    parameterNamesA = ['Atrial Amplitude', 'Atrial Pulse Width']
    parameterNamesV = ['Ventricular Amplitude', 'Ventricular Pulse Width']
    parameterNamesAI = ['Atrial Sensitivity', 'ARP',
                        'PVARP', 'Hysteresis', 'Rate Smoothing']
    parameterNamesVI = ['Ventricular Sensitivity',
                        'VRP', 'Hysteresis', 'Rate Smoothing']
    parameterNamesR = ['Maximum Sensor Rate', 'Activity Threshold',
                       'Reaction Time', 'Response Factor', 'Recovery Time']
    parameterNamesDDDRextra = ['Atrial Sensitivity', 'ARP', 'PVARP', 'Ventricular Sensitivity','VRP','Hysteresis',
                      'Rate Smoothing', 'Fixed AV delay', 'Dynamic AV delay', 'Minimum Dynamic AV delay',
                      'Sensed AV delay offset', 'PVARP Extension','ATR Mode','ATR Duration', 'ATR Fallback Time', 'Ventricular Blanking']
    count = 0
    updated_parameters = {}
    if(curMode != "none"):
        for parameter in parameterNamesCommon:
            updated_parameters[parameter] = values[count]
            count += 1
    if("A" in curMode or "DDDR" in curMode):
        for parameter in parameterNamesA:
            updated_parameters[parameter] = values[count]
            count += 1
    if("V" in curMode or "DDDR" in curMode):
        for parameter in parameterNamesV:
            updated_parameters[parameter] = values[count]
            count += 1
    if("AI" in curMode):
        for parameter in parameterNamesAI:
            updated_parameters[parameter] = values[count]
            count += 1
    if("VI" in curMode):
        for parameter in parameterNamesVI:
            updated_parameters[parameter] = values[count]
            count += 1
    if("R" in curMode or "DDDR" in curMode):
        for parameter in parameterNamesR:
            updated_parameters[parameter] = values[count]
            count += 1
    if("DDDR" in curMode):
        for parameter in parameterNamesDDDRextra:
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

    layoutEgram = [
        [sg.Canvas(key='canvasAtr'), sg.Canvas( key='canvasVent')],
        [sg.Button('Back to Parameters Screen'),sg.Button('Update', key='update')]
    ]

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
            [sg.Button('View Egram')],
            [sg.Text('', size=(sizeText, 1)), sg.Text()],
        ]
        parameters = users[curUser].getParameters()
        parameterValues = parameterUtil.getParameterRangeValues()
        layoutCommons = [
            [sg.Text('Lower Rate Limit (ppm)', size=(sizeText, 1)),
             sg.Spin(parameterValues['Lower Rate Limit'], initial_value=parameters['Lower Rate Limit'], readonly=False,  size=sizeText2)],
            [sg.Text('Upper Rate Limit (ppm)', size=(sizeText, 1)),
             sg.Spin(values=parameterValues['Upper Rate Limit'], initial_value=parameters['Upper Rate Limit'], readonly=False,  size=sizeText2)],
        ]
        layoutR = [[sg.Text('Maximum Sensor Rate (ppm)', size=(sizeText, 1)),
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
        layoutAI = [
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
        layoutVI = [
            [sg.Text('Ventricular Sensitivity (mV)', size=(sizeText, 1)),
             sg.Spin(values=parameterValues['Ventricular Sensitivity'], initial_value=parameters['Ventricular Sensitivity'], readonly=False,  size=sizeText2)],
            [sg.Text('VRP (ms)', size=(sizeText, 1)), sg.Spin(
                values=parameterValues['VRP'], initial_value=parameters['VRP'], readonly=False,  size=sizeText2)],
            [sg.Text('Hysteresis (ppm)', size=(sizeText, 1)),
             sg.Spin(values=parameterValues['Hysteresis'], initial_value=parameters['Hysteresis'], readonly=False,  size=sizeText2)],
            [sg.Text('Rate Smoothing (%)', size=(sizeText, 1)),
             sg.Spin(values=parameterValues['Rate Smoothing'], initial_value=parameters['Rate Smoothing'], readonly=False,  size=sizeText2)],
        ]
        layoutDDDRextra = [
            [sg.Text('Atrial Sensitivity (mV)', size=(sizeText, 1)),
             sg.Spin(values=parameterValues['Atrial Sensitivity'], initial_value=parameters['Atrial Sensitivity'], readonly=False,  size=sizeText2)],
            [sg.Text('ARP (ms)', size=(sizeText, 1)), sg.Spin(
                values=parameterValues['ARP'], initial_value=parameters['ARP'], readonly=False,  size=sizeText2)],
            [sg.Text('PVARP (ms)', size=(sizeText, 1)), sg.Spin(
                values=parameterValues['PVARP'], initial_value=parameters['PVARP'], readonly=False,  size=sizeText2)],
            [sg.Text('Ventricular Sensitivity (mV)', size=(sizeText, 1)),
             sg.Spin(values=parameterValues['Ventricular Sensitivity'], initial_value=parameters['Ventricular Sensitivity'], readonly=False,  size=sizeText2)],
            [sg.Text('VRP (ms)', size=(sizeText, 1)), sg.Spin(
                values=parameterValues['VRP'], initial_value=parameters['VRP'], readonly=False,  size=sizeText2)],
            [sg.Text('Hysteresis (ppm)', size=(sizeText, 1)),
             sg.Spin(values=parameterValues['Hysteresis'], initial_value=parameters['Hysteresis'], readonly=False,  size=sizeText2)],
            [sg.Text('Rate Smoothing (%)', size=(sizeText, 1)),
             sg.Spin(values=parameterValues['Rate Smoothing'], initial_value=parameters['Rate Smoothing'], readonly=False,  size=sizeText2)],
            [sg.Text('Fixed AV delay ()', size=(sizeText, 1)),sg.Spin(values=parameterValues['Fixed AV delay'], initial_value=parameters['Fixed AV delay'], readonly=False,  size=sizeText2)], 
            [sg.Text('Dynamic AV delay', size=(sizeText, 1)),sg.Spin(values=parameterValues['Dynamic AV delay'], initial_value=parameters['Dynamic AV delay'], readonly=False,  size=sizeText2)],
            [sg.Text('Minimum Dynamic AV delay', size=(sizeText, 1)),sg.Spin(values=parameterValues['Minimum Dynamic AV delay'], initial_value=parameters['Minimum Dynamic AV delay'], readonly=False,  size=sizeText2)], 
            [sg.Text('Sensed AV delay offset', size=(sizeText, 1)),sg.Spin(values=parameterValues['Sensed AV delay offset'], initial_value=parameters['Sensed AV delay offset'], readonly=False,  size=sizeText2)],
            [sg.Text('PVARP Extension', size=(sizeText, 1)),sg.Spin(values=parameterValues['PVARP Extension'], initial_value=parameters['PVARP Extension'], readonly=False,  size=sizeText2)],
            [sg.Text('ATR Mode', size=(sizeText, 1)),sg.Spin(values=parameterValues['ATR Mode'], initial_value=parameters['ATR Mode'], readonly=False,  size=sizeText2)], 
            [sg.Text('ATR Duration', size=(sizeText, 1)),sg.Spin(values=parameterValues['ATR Duration'], initial_value=parameters['ATR Duration'], readonly=False,  size=sizeText2)],
            [sg.Text('ATR Fallback Time', size=(sizeText, 1)),sg.Spin(values=parameterValues['ATR Fallback Time'], initial_value=parameters['ATR Fallback Time'], readonly=False,  size=sizeText2)],
            [sg.Text('Ventricular Blanking', size=(sizeText, 1)),sg.Spin(values=parameterValues['Ventricular Blanking'], initial_value=parameters['Ventricular Blanking'], readonly=False,  size=sizeText2)],
        ]
        layoutFooter = [[sg.Button('Submit Parameters')],
                        [sg.Button('Log Off')]]
    if (state == "login"):
        return sg.Window('PaceMaker', layoutLogin, resizable=True)
    elif (state == "control"):
        if(logging):
            print(event)
        layoutControl = [layoutHeader]
        if("A" in curMode):
            layoutControl.append(layoutCommons)
            layoutControl.append(layoutA)
        if("V" in curMode):
            layoutControl.append(layoutCommons)
            layoutControl.append(layoutV)
        if("AI" in curMode):
            layoutControl.append(layoutAI)
        if("VI" in curMode):
            layoutControl.append(layoutVI)
        if("R" in curMode):
            layoutControl.append(layoutR)
        if("DDDR" in curMode):
            layoutControl = []
            temp = [layoutHeader,layoutCommons, layoutA, layoutV, layoutR, layoutDDDRextra, layoutFooter]

            for listLayout in temp:
                for element in listLayout:
                    layoutControl.append(element)
            
            layout = [
                [sg.Column(layoutControl, scrollable=True,  vertical_scroll_only=True)]
            ]
            return sg.Window('PaceMaker', layout, resizable=True)
        layoutControl.append(layoutFooter)
        return sg.Window('PaceMaker', layoutControl, resizable=True)
    elif (state == "createUser"):
        return sg.Window('PaceMaker', layoutCreateUser, resizable=True)
    elif (state == "egram"):
        return sg.Window('PaceMaker', layoutEgram,
                           resizable=True, finalize=True, location=(115, 125), element_justification='center')

# main function to run GUI
if __name__ == '__main__':
    # try:
        dataBaseFile = updateDataBaseFile()
        sg.theme('LightGrey1')
        window = getWindowByState()
        defaultEgramData()
        counter = 0

        while True: 
            event, values = window.read(timeout=100)
            # print(counter)
            counter += 1
            if event == sg.WIN_CLOSED or event == 'Cancel':
                window.close()
                break
            if (logging):
                print(state) 
                print(event)
                print(values)
            if (state == "login"):
                getAllUsers()
                if (event == "Login"):
                    if (users.get(getRealValue(values[0])) and users[getRealValue(values[0])].checkCredential(getRealValue(values[0]), getRealValue(values[1]))):
                        infoMessage = ""
                        state = "control"
                        curUser = getRealValue(values[0])
                        infoMessage = "Welcome to Control Panel for: " + curUser
                        windowMode = users[getRealValue(values[0])].getMode()
                        curMode = users[getRealValue(values[0])].getMode()
                        window.close()
                        window = getWindowByState()
                    else:
                        infoMessage = "Password Incorrect or this user does not exist"
                        window.close()
                        window = getWindowByState()
                elif (event == "Create New User"):
                    infoMessage = ""
                    state = "createUser"
                    window.close()
                    window = getWindowByState()
            elif (state == "createUser"):
                if (event == "Create New User"):
                    if (not (getRealValue(values[1]) == getRealValue(values[2]))):
                        infoMessage = "Password mismatch"
                    elif (not checkValid(values[0]) == None):
                        infoMessage = checkValid(values[0])
                    elif (not checkValid(values[1]) == None):
                        infoMessage = checkValid(values[1])
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
                    window.close()
                    window = getWindowByState()
                elif (event == "Back to Login"):
                    state = "login"
                    window.close()
                    window = getWindowByState()
            elif (state == "control"):
                windowMode = values['mode']
                if(windowMode in mode):
                    curMode = windowMode
                    window.close()
                    window = getWindowByState()
                if (event == "Submit Parameters"):
                    newParameters = getUpdatedParameters(values)
                    check = parameterUtil.checkParameterInRange(newParameters)
                    if(check == None):
                        users[curUser].updateParameters(newParameters)
                        users[curUser].setMode(curMode)
                        infoMessage = "Parameters Successfully Updated!"
                        updateDatabase()
                        getAllUsers()
                        serialCommunicate()
                    else:
                        infoMessage = "Double check the value entered are in range for parameter: " + \
                            str(check)
                    window.close()
                    window = getWindowByState()
                if (event == "View Egram"):
                    state = "egram"
                    infoMessage = ""
                    window.close()
                    path = serialCommunicate(True)
                    window = getWindowByState()
                    spectraPlot1 = updateable_matplotlib_plot(window['canvasAtr'], "Egram Data Atr")
                    spectraPlot2 = updateable_matplotlib_plot(window['canvasVent'], "Egram Data Vent")
                    window.finalize()
                    spectraPlot1.plot(egramData['atr']) 
                    spectraPlot2.plot(egramData['vent']) 
                if (event == "Log Off"):
                    state = "login"
                    infoMessage = "Successful log off"
                    window.close()
                    window = getWindowByState()
            elif (state == "egram"):
                # tempData()
                readEgramData(path)
                spectraPlot1.plot(egramData['atr']) 
                spectraPlot2.plot(egramData['vent']) 
                if event == "update":
                    spectraPlot1.plot(egramData['atr']) 
                    spectraPlot2.plot(egramData['vent']) 
                if (event == "Back to Parameters Screen"):
                    state = "control"
                    infoMessage = "Welcome to Control Panel for: " + curUser
                    window.close()
                    window = getWindowByState()
        window.close()
    # except Exception as e:
    #     window.close()
    #     sg.popup_error_with_traceback(
    #         "An error had occured. Please contact the support team with the following info: ", e)
