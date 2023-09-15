import PySimpleGUI as sg

sg.theme('DarkAmber')
layout = [[sg.Text('Name'), sg.InputText()],
          [sg.Text('Password'), sg.InputText()],
          [sg.Button('Login'), sg.Button('Create New User')]]

window = sg.Window('PaceMaker', layout)


class Users:
    def __init__(self, name, age):
        self.name = name
        self.age = age


while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break
    print('You entered ', values)

window.close()
