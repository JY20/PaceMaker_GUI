import PySimpleGUI as sg
import csv

usersCredentials = {}
logging = False
state = "login"
infoMessage = ""
dataBaseFile = "database.csv"
windowSize = []


class Users:
    def __init__(self, name, password):
        self.name = name
        self.password = password

    def checkCredential(self, name, password):
        if (self.name == name and self.password == password):
            return True
        else:
            return False


def getRealValue(value):
    return value.replace(" ", "").replace("\n", "")


def createUserDB(name, password):
    f = open(dataBaseFile, "a")
    value = name+","+password+"\n"
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
                usersCredentials[getRealValue(
                    values[0])] = getRealValue(values[1])
                if (logging):
                    print("user: "+str(values))
    f.close()


def getWindowByState():
    sizeText = 10
    layoutLogin = [[sg.Text(infoMessage), sg.Text()],
                   [sg.Text('Name', size=(sizeText, 1)), sg.InputText()],
                   [sg.Text('Password', size=(sizeText, 1)), sg.InputText()],
                   [sg.Text('', size=(sizeText, 1)), sg.Text()],
                   [sg.Button('Login'), sg.Button('Create New User')]]

    sizeText = 50
    layoutControl = [
        [sg.Text("Welcome to Control Panel!"), sg.Text()]]
    sizeText = 20
    layoutCreateUser = [
        [sg.Text(infoMessage), sg.Text()],
        [sg.Text('Name', size=(sizeText, 1)), sg.InputText()],
        [sg.Text('Password', size=(sizeText, 1)), sg.InputText()],
        [sg.Text('Confirm Password', size=(sizeText, 1)), sg.InputText()],
        [sg.Text('', size=(sizeText, 1)), sg.Text()],
        [sg.Button('Create New User')], [sg.Button('Back to Login')]]

    if (state == "login"):
        window = sg.Window('PaceMaker', layoutLogin, resizable=True)
        return window
    elif (state == "control"):
        window = sg.Window('PaceMaker', layoutControl, resizable=True)
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

        # windowSize = window.size

        if (logging):
            print(state)

        if (state == "login"):
            getAllUsers()
            if (event == "Login"):
                if (logging):
                    print(values)
                if (usersCredentials[getRealValue(values[0])] == getRealValue(values[1])):
                    infoMessage = ""
                    state = "control"
                else:
                    infoMessage = "Password Incorrect"
            elif (event == "Create New User"):
                infoMessage = ""
                state = "createUser"
        elif (state == "createUser"):
            if (event == "Create New User"):
                if (not (getRealValue(values[1]) == getRealValue(values[2]))):
                    infoMessage = "Password mismatch"
                elif (usersCredentials.get(getRealValue(values[0]))):
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
        window.close()
    window.close()
