import hashlib

class Login:

    mail = ""
    password = ""
    hashed = ""

    def __init__(self, mail, password):
        self.mail = mail
        self.password = password

    def getHash(self):
        return self.hashed

    def hashPassword(self):
        pw = self.password.encode('utf-8')
        self.hashed = hashlib.sha256(pw).hexdigest()
