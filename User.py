class User:
    def __init__(self, name, password):
        self.name = name
        self.password = password

    def checkCredential(self, name, password):
        if(self.name == name and self.password == password):
            return True
        else:
            return False
