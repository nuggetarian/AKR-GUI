from email_pokus import sendEmail
from login import Login
import os
from sys import platform
import getpass
from login import Login
import logging
import bcrypt
from sqliteoperations import Database

def clearscreen():
    if platform == 'win32':
        os.system('cls') 
    elif platform == 'darwin':
        os.system('clear') 
    elif platform == 'linux':
        os.system('clear') 
    
def menu():
      print("1. Zobrazit hesla")
      print("2. Pridat heslo")
      print("3. Zmazat heslo")
      print("0. Odhlasit")

def firstScreen():
    print("1. Prihlasit sa")
    print("2. Registrovat sa")
    print("0. Exit")

#PREMENNE
mail = ""
password = ""
logging.basicConfig(filename="logfile.log",
                    format='%(asctime)s %(message)s',
                    filemode='a')
logger=logging.getLogger()
logger.setLevel(logging.DEBUG)

firstScreen()
choice = int(input("Zvol moznost:"))
while choice != 0:
    if choice == 1:
        clearscreen()
        logger.info("Log in chosen")
        print("Zadaj email: ")
        mail = input()
        password = getpass.getpass(prompt='Zadaj heslo:')
        database = Database(mail, password)
        if database.comparePasswords() == True:
            #clearscreen()
            #Posielanie mailu, DOCASNE VYPNUTE
            #se = sendEmail()
            #se.send_email(mail) 
            print("Zadaj kod:")
            x = input()
            if x == str(se.getMessage()):
                print("Spravny kod")
                logger.info("Successful login")
                input("====Stlač enter====")
                clearscreen()
                menu()
                volba = int(input("Zvol moznost:"))

                while volba != 0:
                    if volba == 1:
                        print("Zvolil si zobrazenie hesiel")
                        logger.info("Passwords viewed")
                        input("====Stlac enter====")
                    elif volba == 2:
                        print("Zvolil si pridanie hesla.")
                        logger.info("Password added")
                        input("====Stlac enter====")
                    elif volba == 3:
                        print("Zvolil si zmazanie hesla")
                        logger.info("Password deleted")
                        input("====Stlac enter====")
                    else:
                        print("Nespravna volba.")
                        input("====Stlac enter====")
                    clearscreen()
                    menu()
                    try:
                        volba = int(input("Zvol moznost:"))
                    except:
                        print("Nespravny input.")
                        break
                print("Logging out.")
                logger.info("Log out")

            elif x != str(se.getMessage()):
                print("Nespravny kod")
                logger.info("Unsuccessful login")
        elif database.comparePasswords() == False:
            print("Nespravne heslo")
            input("====Stlac enter====")

    elif choice == 2:
        logger.info("Sign up chosen")
        print("Zadaj email: ")
        mail = input()
        password = getpass.getpass(prompt='Zadaj heslo:')
        database = Database(mail, password)
        database.addValues()

    else:
        print("Nespravna volba.")
        input("====Stlac enter====")

    clearscreen()
    firstScreen()
    try:
        choice = int(input("Zvol moznost:"))
    except:
        print("Nespravny input.")
        break
print("Exit.")
logger.info("Quit")












