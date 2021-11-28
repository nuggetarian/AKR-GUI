import sqlite3
from tkinter import *
from tkinter import ttk
from pwdatabase import PwDatabase
from userdatabase import Database
import os
import logging
from PIL import ImageTk, Image
from email_pokus import sendEmail
from Crypto.Cipher import AES
from treeview import treeViewDB
from encryption import Encryption
from checksum import CheckSum

absolutepath = os.path.abspath(__file__)
fileDirectory = os.path.dirname(absolutepath)

# Deklaracia hlavneho okna
master = Tk()
master.title("Password Manager")
master.iconbitmap(fileDirectory + "\\pictures\\lock.ico")

# Logger na zapis akcii
logging.basicConfig(filename="logfile.log",
                    format='%(asctime)s %(message)s',
                    filemode='a')
logger=logging.getLogger()
logger.setLevel(logging.DEBUG)
logging.getLogger('PIL').setLevel(logging.WARNING)


def firstScreen(): # Hlavna obrazovka pri spusteni
  master.title("Password Manager") # Nazov okna
  master.iconbitmap(fileDirectory + "\\pictures\\lock.ico") # Ikonka okna
  master.geometry("500x500") # Rozmery okna
  master.configure(background="white") # Konfiguracia okna (napr. biele pozadie)
  for widget in master.winfo_children(): # Je potrebne vzdy znicit vsetky widgety, inak by sa v okne stale skladali pod seba
    widget.destroy()

  # Logo FEKT
  fekt_img = Image.open(fileDirectory + '\\pictures\\fekt.png')
  fekt_img = fekt_img.resize((342,111), Image.ANTIALIAS)
  fekt_img = ImageTk.PhotoImage(fekt_img)
  fekt_label = ttk.Label(image=fekt_img)
  fekt_label.image = fekt_img
  fekt_label.config(anchor=CENTER, background="white")
  fekt_label.pack()

  global logInImage # Tlacitko na prihlasenie
  logInImage = PhotoImage(file=fileDirectory + '\\pictures\\login.png')
  logInBtn = Button(master, image=logInImage, command=logInScreen, borderwidth=0, cursor="hand2", activebackground="#fff")
  logInBtn.config(background="white")
  logInBtn.pack(pady=5)
  
  global signUpImage # Tlacitko na registraciu
  signUpImage = PhotoImage(file=fileDirectory + '\\pictures\\signup.png')
  signUpBtn = Button(master, image=signUpImage, command=signUpScreen, borderwidth=0, cursor="hand2", activebackground="#fff")
  signUpBtn.configure(background="white")  
  signUpBtn.pack(pady=5)

  def saveEndExit(): # Funkcia ktora overi existenciu databazy, zasifruje ju a ukonci program
    file_exists = os.path.exists('users.db')
    if file_exists == True:
      e = Encryption()
      e.aes128Encrypt('users', "aE3xCj83")
      logger.info("App exited")
      master.quit()
    elif file_exists == False:
      print("File does not exist")
      logger.info("App exited")
      master.quit()

  # Tlacitko na zasifrovanie a ukoncenie programu
  global saveAndExitImage
  saveAndExitImage = PhotoImage(file=fileDirectory + '\\pictures\\saveaexit.png')
  saveAndExitButton = Button(master, image=saveAndExitImage, cursor="hand2", command=saveEndExit,  borderwidth=0, activebackground="#fff")
  saveAndExitButton.config(background="white")
  saveAndExitButton.pack(pady=5)

def signUpScreen(): # Obrazovka registracie
  logger.info("Sign up chosen")
  for widget in master.winfo_children():
    widget.destroy()
  master.geometry("500x500")

  # Napis mail
  mailLbl = Label(master, text="E-mail:", font="Helvetica 14 bold", background="white")
  mailLbl.config(anchor=CENTER)
  mailLbl.pack(pady=5)

  # Pole na vyplnenie mailu
  mailEntry = Entry(master, width=30, font="Helvetica", borderwidth=2)
  mailEntry.pack(pady=5)

  # Napis hesla
  passwordLbl = Label(master, text="Password:", font="Helvetica 14 bold", background="white")
  passwordLbl.config(anchor=CENTER)
  passwordLbl.pack(pady=5)

  # Pole na vyplnenie hesla
  passwordEntry = Entry(master, show="*", width=30, font="Helvetica", borderwidth=2)
  passwordEntry.pack()

  # Napis subor - pomenujeme subor, ktory bude nasa databaza hesiel
  filenameLbl = Label(master, text="Filename:", font="Helvetica 14 bold", background="white")
  filenameLbl.config(anchor=CENTER)
  filenameLbl.pack(pady=5)

  # Pole na vyplnenie suboru
  filenameEntry = Entry(master, width=30, font="Helvetica", borderwidth=2)
  filenameEntry.pack()

  def addToDatabase(encryption): # Funkcia na pridanie informacii do databazoveho suboru o uzivateloch
    signUpMail = mailEntry.get().strip()
    signUpPassword = passwordEntry.get()
    signUpFilename = filenameEntry.get().strip()
    # Chceme zamedzit specialne znaky pri tvoreni mena suboru
    signUpFilename = ''.join(char for char in signUpFilename if char.isalnum()) 
    db = Database(signUpMail, signUpPassword)
    db.createTable()
    pwdb = PwDatabase()
    try: 
      db.addValues(signUpFilename, encryption)
      pwdb.createTable(signUpFilename)
      firstScreen()
      success = Label(master, text="Registrácia prebehla úspešne.", font="Helvetica", background="white")
      logger.info("User signed up with mail " + signUpMail)
      success.config(anchor=CENTER)
      success.pack(pady = 5)
      # Na zaklade zvolenej sifry zasifrujeme subor, zapiseme do logu
      if encryption == "des168":
        logger.info("3DES 168bit selected")
        e.threeDes168Encrypt(signUpFilename, signUpPassword)
      elif encryption == "des112":
        logger.info("3DES 112bit selected")
        e.threeDes112Encrypt(signUpFilename, signUpPassword)
      elif encryption == "chacha128":
        e.chaCha128Encrypt(signUpFilename, signUpPassword)
      elif encryption == "chacha256":
        logger.info("ChaCha 256bit selected")
        e.chaCha256Encrypt(signUpFilename, signUpPassword)
      elif encryption == "aes128":
        logger.info("AES 128bit selected")
        e.aes128Encrypt(signUpFilename, signUpPassword)
      elif encryption == "aes256":
        logger.info("AES 256bit selected")
        e.aes256Encrypt(signUpFilename, signUpPassword)
    except sqlite3.IntegrityError: # Ak sa email pouziva sqlite vyhodi error, kedze v databaze take data uz su
      logger.info("Unsuccessful sign up with mail " + signUpMail + ": this e-mail already exists")
      warningLabel = Label(master, text="E-mail sa už používa.", font="Helvetica", background="white")
      warningLabel.config(anchor=CENTER)
      warningLabel.pack(pady=5)
    except sqlite3.DatabaseError: # Ak sa nazov suboru pouziva, taktiez sqlite vyhodi error
      logger.info("Unsuccessful sign up with mail " + signUpMail + ": this filename already exists")
      warningLabel = Label(master, text="Názov databázy sa už používa.", font="Helvetica", background="white")
      warningLabel.config(anchor=CENTER)
      warningLabel.pack(pady=5)

  # Napis objasnujuci dalsi krok (zvolenie sifrovacieho algoritmu)
  chooseEncryptionLbl = Label(text="Zvoľ šifrovací algoritmus a dĺžku \nkľúča na ukončenie registrácie:", font="Helvetica 12", background="white")
  chooseEncryptionLbl.config(anchor=CENTER)
  chooseEncryptionLbl.pack(pady=5)

  # Mriezka na utriedenie tlacitok
  buttonGrid = LabelFrame(master, borderwidth=0, background="white")
  buttonGrid.pack()
  e = Encryption()

  # Orazky tlacitok
  global des112Image
  global des168Image
  global aes128Image
  global aes256Image
  global chacha128Image
  global chacha256Image
  des112Image = PhotoImage(file=fileDirectory + '\\pictures\\3des112-1.png')
  des168Image = PhotoImage(file=fileDirectory + '\\pictures\\3des168-1.png')
  aes128Image = PhotoImage(file=fileDirectory + '\\pictures\\aes128-1.png')
  aes256Image = PhotoImage(file=fileDirectory + '\\pictures\\aes256-1.png')
  chacha128Image = PhotoImage(file=fileDirectory + '\\pictures\\chacha128-1.png')
  chacha256Image = PhotoImage(file=fileDirectory + '\\pictures\\chacha256-1.png')

  # Tlacitka na vyber sifry
  des112Button = Button(buttonGrid, image=des112Image, background="white", cursor="hand2", borderwidth=0, command=lambda: addToDatabase("des112"), activebackground="#fff").grid(row=0, column=0, padx=10, pady=10)
  des168Button = Button(buttonGrid, image=des168Image, background="white", cursor="hand2", borderwidth=0, command=lambda: addToDatabase("des168"), activebackground="#fff").grid(row=1, column=0, padx=10, pady=10)
  #chaCha128Button = Button(buttonGrid, image=chacha128Image, background="white", cursor="hand2", borderwidth=0, command=lambda: addToDatabase("chacha128"), activebackground="#fff").grid(row=0, column=1, padx=10, pady=10)
  chaCha256Button = Button(buttonGrid, image=chacha256Image, background="white", cursor="hand2", borderwidth=0, command=lambda: addToDatabase("chacha256"), activebackground="#fff").grid(row=0, column=1, padx=10, pady=10)
  aes128Button = Button(buttonGrid, image=aes128Image, background="white", cursor="hand2", borderwidth=0, command=lambda: addToDatabase("aes128"), activebackground="#fff").grid(row=0, column=2, padx=10, pady=10)
  aes256Button = Button(buttonGrid, image=aes256Image, background="white", cursor="hand2", borderwidth=0, command=lambda: addToDatabase("aes256"), activebackground="#fff").grid(row=1, column=2, padx=10, pady=10)

  # Tlacitko na navrat na hlavnu obrazovku
  global backImage
  backImage = PhotoImage(file=fileDirectory + '\\pictures\\back.png')
  backButton = Button(master, image=backImage, command=firstScreen, cursor="hand2", borderwidth=0, background="white", activebackground="#fff").pack(pady=5)

def treeViewDatabase(filename): # Zobrazenie databazy s heslami v specialnom okne
  for widget in master.winfo_children():
    widget.destroy()
  master.geometry("550x600")
  master.title("Vault")
  master.resizable(False, True)
  master.iconbitmap(fileDirectory + "\\pictures\\unlocked_lock.ico")
  logger.info("Database viewed")

  def saveAndEncrypt(): # Ked ukoncime prezeranie, na zaklade zvolenej sifry zasifrujeme subor s heslami
    e = Encryption()
    db.addChecksumValues(db.findFile(mail))
    if db.findEncryption(mail) == 'des168':
      e.threeDes168Encrypt(db.findFile(mail), password)
      e.aes128Encrypt('users', "aE3xCj83")
      logger.info("App exited")
      master.quit()
    elif db.findEncryption(mail) == 'des112':
      e.threeDes112Encrypt(db.findFile(mail), password)
      e.aes128Encrypt('users', "aE3xCj83")
      logger.info("App exited")
      master.quit()
    elif db.findEncryption(mail) == 'chacha128':
      e.chaCha128Encrypt(db.findFile(mail), password)
      e.aes128Encrypt('users', "aE3xCj83")
      logger.info("App exited")
      master.quit()
    elif db.findEncryption(mail) == 'chacha256':
      e.chaCha256Encrypt(db.findFile(mail), password)
      e.aes128Encrypt('users', "aE3xCj83")
      logger.info("App exited")
      master.quit()
    elif db.findEncryption(mail) == 'aes128':
      e.aes128Encrypt(db.findFile(mail), password)
      e.aes128Encrypt('users', "aE3xCj83")
      logger.info("App exited")
      master.quit()
    elif db.findEncryption(mail) == 'aes256':
      e.aes256Encrypt(db.findFile(mail), password)
      e.aes128Encrypt('users', "aE3xCj83")
      logger.info("App exited")
      master.quit()

  # Z triedy treeviewDB volame funkciu viewFromDatabase
  tree = treeViewDB()
  tree.viewFromDatabase(master, filename)
  # Obrazok a tlacitko na ulozenie a zasifrovanie databazy
  global saveEncryptImage
  saveEncryptImage = PhotoImage(file=fileDirectory + '\\pictures\\saveencrypt.png')
  save_encrypt_button = Button(master, command=saveAndEncrypt, image=saveEncryptImage, cursor="hand2", borderwidth=0, background="white", activebackground="#fff")
  save_encrypt_button.pack(pady=5)

def logInScreen(): # Prihlasovacie okno
  logger.info("Log in chosen")

  for widget in master.winfo_children():
    widget.destroy()
  master.geometry("500x500")

  # Napis mail
  mailLbl = Label(master, text="E-mail:", font="Helvetica 14 bold")
  mailLbl.config(anchor=CENTER, background="white")
  mailLbl.pack(pady=5)

  # Pole na vyplnenie mailu
  mailEntry = Entry(master, width=30, font="Helvetica", borderwidth=2)
  mailEntry.pack(pady=5)

  # Napis heslo
  passwordLbl = Label(master, text="Password:", font="Helvetica 14 bold")
  passwordLbl.config(anchor=CENTER, background="white")
  passwordLbl.pack(pady=5)

  # Pole na vyplnenie hesla
  passwordEntry = Entry(master, show="*", width=30, font="Helvetica", borderwidth=2)
  passwordEntry.pack()

  def comparePasswords(): # Funkcia na porovnanie hesiel
    # Globalne premenne aby sme ziskane data mohli posunut do dalsich okien
    try:
      global mail
      mail = mailEntry.get().strip()
      global password
      password = passwordEntry.get()
      global db
      db = Database(mail, password)
      if (db.comparePasswords() == True):
        logger.info("Log in successful as " + mail)
        global se
        se = sendEmail()
        se.send_email(mail) # Odoslanie mailu s overovacim kodom
        twoFactorPopUp() # Okno na vyplnenie overovacieho kodu
      else:
        logger.info("Log in unsuccessful as " + mail)
        popUp() # Pop Up, ze sme zadali nespravne heslo
    except: # Ak sa mail nenachadza v databaze, vypiseme tuto informaciu na obrazovku
        logger.info("Unsuccessful log up with mail " + mail + ": e-mail isn't in the database")
        warningLabel = Label(master, text="E-mail sa nenachádza v databáze.", font="Helvetica", background="white")
        warningLabel.config(anchor=CENTER)
        warningLabel.pack(pady=5)

  # Tlacidlo na funkciu comparePasswords
  global submitImage
  submitImage = PhotoImage(file=fileDirectory + '\\pictures\\submit.png')
  submitButton = Button(master, image=submitImage, command=comparePasswords, cursor="hand2", borderwidth=0, background="white", activebackground="#fff").pack(pady=5)

  # Tlacidlo na navrat do hlavneho okna
  global backImage
  backImage = PhotoImage(file=fileDirectory + '\\pictures\\back.png')
  backButton = Button(master, image=backImage, command=firstScreen, cursor="hand2", borderwidth=0, background="white", activebackground="#fff").pack(pady=5)

def popUp(): # Pop Up okno, ze sme zadali nespravne heslo
  popUpWindow = Toplevel(master)
  popUpWindow.geometry("250x50")
  popUpWindow.title("Warning")
  popUpWindow.resizable(False, False) # Zakaz menit velkost okna
  popUpWindow.config(background="white")
  popUpWindow.iconbitmap(fileDirectory + "\\pictures\\warning.ico")
  # Napis oznamujuci zle zadane heslo
  warningLbl = Label(popUpWindow, text="NESPRÁVNE HESLO", font="Helvetica 10")
  warningLbl.config(anchor=CENTER, background="white")
  warningLbl.pack(pady=5)

def twoFactorPopUp(): # Dvojfaktorove overenie - okno
  for widget in master.winfo_children():
    widget.destroy()
  master.geometry("500x500")

  # Napis aby sme zadali kod z mailu
  verificationLbl = Label(master, text="Zadaj kód z mailu:", font="Helvetica 14 bold", background="white")
  verificationLbl.config(anchor=CENTER)
  verificationLbl.pack(pady=5)

  # Pole na zadanie kodu
  codeEntry = Entry(master, width=30, font="Helvetica", borderwidth=2)
  codeEntry.pack(pady=5)

  def codeVerification(): # Overenie kodu a desifrovanie 
    if codeEntry.get().strip() == se.getMessage():
      e = Encryption()
      if db.findEncryption(mail) == 'des168':
        e.threeDes168Decrypt(db.findFile(mail), password)
        treeViewDatabase(db.findFile(mail))
        popUpChecksum()
      elif db.findEncryption(mail) == 'des112':
        e.threeDes112Decrypt(db.findFile(mail), password)
        treeViewDatabase(db.findFile(mail))
        popUpChecksum()
      elif db.findEncryption(mail) == 'chacha128':
        e.chaCha128Decrypt(db.findFile(mail), password)
        treeViewDatabase(db.findFile(mail))
        popUpChecksum()
      elif db.findEncryption(mail) == 'chacha256':
        e.chaCha256Decrypt(db.findFile(mail), password)
        treeViewDatabase(db.findFile(mail))
        popUpChecksum()
      elif db.findEncryption(mail) == 'aes128':
        e.aes128Decrypt(db.findFile(mail), password)
        treeViewDatabase(db.findFile(mail))
        popUpChecksum()
      elif db.findEncryption(mail) == 'aes256':
        e.aes256Decrypt(db.findFile(mail), password)
        treeViewDatabase(db.findFile(mail))
        popUpChecksum()
    else: # Zadanie nespravneho kodu
      warningLbl = Label(master, text="Nesprávny kód.", font="Helvetica", background="white")
      warningLbl.config(anchor=CENTER)
      warningLbl.pack()

  # Tlacidlo na potvrdenie
  global submitImage
  submitImage = PhotoImage(file=fileDirectory + '\\pictures\\submit.png')
  okButton = Button(master, image=submitImage, command=codeVerification, borderwidth=0, cursor="hand2", activebackground="#fff", background="white").pack(pady=5)

  # Tlacidlo na navrat do hlavneho okna
  global backImage
  backImage = PhotoImage(file=fileDirectory + '\\pictures\\back.png')
  backButton = Button(master, image=backImage, command=firstScreen, cursor="hand2", borderwidth=0, background="white", activebackground="#fff").pack(pady=5)

def decryptUsers(): # Desifrovanie databazy uzivatelov
  file_exists = os.path.exists('users.db')
  if file_exists == True: # Otestujeme ci dany subor existuje
    print("File exists")
    e = Encryption()
    e.aes128Decrypt('users', "aE3xCj83")
  elif file_exists == False:
    print("File does not exist")

def popUpChecksum(): # Pop Up okno na overenie integrity suboru
  popUpWindow = Toplevel(master)
  popUpWindow.geometry("400x100")
  popUpWindow.title("Checksum")
  popUpWindow.resizable(False, False) # Neda sa zmenit velkost
  popUpWindow.config(background="white")
  popUpWindow.iconbitmap(fileDirectory + "\\pictures\\warning.ico")
  checksum = CheckSum() 
  
  # Overujeme checksum ulozeny v databaze users.db, ktory sa vytvoril ked sme ulozili subor a checksum vytvoreny pri zavolani funkcie,
  # aby sme zistili ci sa so suborom manipulovalo mimo aplikacie alebo nie. Ak ano, pop up nam to oznami.
  try: 
    if db.findChecksum(db.findFile(mail)) == checksum.get_checksum(db.findFile(mail)):
        warningLbl = Label(popUpWindow, text="Integrita overená: súbor je správny.", font="Helvetica 10")
        warningLbl.config(anchor=CENTER, background="white")
        warningLbl.pack(pady=5)
    elif db.findChecksum(db.findFile(mail)) != checksum.get_checksum(db.findFile(mail)):
        warningLbl = Label(popUpWindow, text="Integrita neoverená: súbor bol buď pozmenený, alebo je nový.", font="Helvetica 10")
        warningLbl.config(anchor=CENTER, background="white")
        warningLbl.pack(pady=5)
  except IndexError:
    print("No checksum yet.")

decryptUsers() # Desifrovanie databaze uzivatelov ked otvorime aplikaciu.
firstScreen() # Zavolanie prveho okna
master.mainloop() 

#To DO
# Fixnut vecicky
# Same id treeview chybova hlaska sqlite3.IntegrityError, alebo id nebolo zadane
# Strip id treeview