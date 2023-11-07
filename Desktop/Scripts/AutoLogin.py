from os.path import exists
from os import system, remove

class AutoLogin:
    def __init__(self):
        if exists(".autologin.txt"):
            self.exist = True
            file = open(".autologin.txt", "r", encoding="utf-8")
            try:
                line = file.readline().split()
                self.login = line[0].replace("_"," ")
                self.passwd = line[1]
            except:
                self.exist = False
        else:
            self.exist = False
        
    def get_login_data(self) -> (tuple | None):
        try:
            return (self.login, self.passwd)
        except:
            return None

    def set_new_data(self, login:str, password:str):
        login = login.replace(" ", "_")
        file = open(".autologin.txt", "w", encoding="utf-8")
        system("attrib +h .autologin.txt")
        file.write(login)
        file.write(" ")
        file.write(password)

    def del_current_data():
        if exists(".autologin.txt"):
            remove(".autologin.txt")

    def is_exist(self) -> bool:
        return self.exist