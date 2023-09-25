import PySimpleGUI as sg
import csv
import hashlib

from User import User

users = {}
logging = True
state = "login"
mode = ["AOOR", "AAIR", "VOOR", "VVIR"]
infoMessage = ""
dataBaseFile = "database.csv"
curUser = ""


def getRealValue(value):
    return value.replace(" ", "").replace("\n", "")


def createUserDB(name, password):
    f = open(dataBaseFile, "a")
    value = name+","+hashlib.sha256(password.encode('utf-8')).hexdigest()+"\n"
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
                users[getRealValue(
                    values[0])] = User(getRealValue(
                        values[0]), getRealValue(
                        values[1]))
                if (logging):
                    print("user: "+str(values))
    f.close()


def getWindowByState():
    sizeText = 10
    layoutLogin = [[sg.Text(infoMessage), sg.Text()],
                   [sg.Text('Name', size=(sizeText, 1)), sg.InputText()],
                   [sg.Text('Password', size=(sizeText, 1)),
                    sg.InputText(password_char='*')],
                   [sg.Text('', size=(sizeText, 1)), sg.Text()],
                   [sg.Button('Login'), sg.Button('Create New User')]]

    sizeText = 20
    layoutCreateUser = [
        [sg.Text(infoMessage), sg.Text()],
        [sg.Text('Name', size=(sizeText, 1)), sg.InputText()],
        [sg.Text('Password', size=(sizeText, 1)),
         sg.InputText(password_char='*')],
        [sg.Text('Confirm Password', size=(sizeText, 1)),
         sg.InputText(password_char='*')],
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

    layoutCommonParameters = [
        [sg.Text('Lower Rate Limit', size=(sizeText, 1)), sg.InputText()],
        [sg.Text('Upper Rate Limit', size=(sizeText, 1)), sg.InputText()],
        [sg.Text('Maximum Sensor Rate', size=(sizeText, 1)), sg.InputText()],
        [sg.Text('Activity Threshold', size=(sizeText, 1)), sg.InputText()],
        [sg.Text('Reaction Time', size=(sizeText, 1)), sg.InputText()],
        [sg.Text('Response Factor', size=(sizeText, 1)), sg.InputText()],
        [sg.Text('Recovery Time', size=(sizeText, 1)), sg.InputText()],
    ]
    layoutA = [
        [sg.Text('Atrial Amplitude', size=(sizeText, 1)), sg.InputText()],
        [sg.Text('Atrial Pulse Width', size=(sizeText, 1)), sg.InputText()],
    ]
    layoutV = [
        [sg.Text('Ventricular Amplitude', size=(sizeText, 1)), sg.InputText()],
        [sg.Text('Ventricular Pulse Width', size=(sizeText, 1)), sg.InputText()],
    ]
    layoutAIR = [
        [sg.Text('Atrial Sensitivity', size=(sizeText, 1)), sg.InputText()],
        [sg.Text('ARP', size=(sizeText, 1)), sg.InputText()],
        [sg.Text('PVARP', size=(sizeText, 1)), sg.InputText()],
        [sg.Text('Hysteresis', size=(sizeText, 1)), sg.InputText()],
        [sg.Text('Rate Smoothing', size=(sizeText, 1)), sg.InputText()],
    ]
    layoutVIR = [
        [sg.Text('Ventricular Sensitivity', size=(sizeText, 1)), sg.InputText()],
        [sg.Text('VRP', size=(sizeText, 1)), sg.InputText()],
        [sg.Text('Hysteresis', size=(sizeText, 1)), sg.InputText()],
        [sg.Text('Rate Smoothing', size=(sizeText, 1)), sg.InputText()],
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
        if (event == 0):
            window = sg.Window('PaceMaker', layoutAOOR, resizable=True)
        elif (event == 1):
            window = sg.Window('PaceMaker', layoutAAIR, resizable=True)
        elif (event == 2):
            window = sg.Window('PaceMaker', layoutVOOR, resizable=True)
        elif (event == 3):
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
            if (event == "Log Off"):
                state = "login"
                infoMessage = "Successful log off"
        window.close()
    window.close()
