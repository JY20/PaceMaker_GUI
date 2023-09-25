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

    def updateParameters(self, newParameters):
        return None
