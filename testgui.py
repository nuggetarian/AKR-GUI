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

absolutepath = os.path.abspath(__file__)
fileDirectory = os.path.dirname(absolutepath)

master = Tk()
master.title("Password Manager")
master.iconbitmap(fileDirectory + "\\pictures\\lock.ico")

# LOGGER
logging.basicConfig(filename="logfile.log",
                    format='%(asctime)s %(message)s',
                    filemode='a')
logger=logging.getLogger()
logger.setLevel(logging.DEBUG)
logging.getLogger('PIL').setLevel(logging.WARNING)

def firstScreen():
  master.title("Password Manager")
  master.iconbitmap(fileDirectory + "\\pictures\\lock.ico")
  master.geometry("500x500")
  master.configure(background="white")
  for widget in master.winfo_children():
    widget.destroy()

  fekt_img = Image.open(fileDirectory + '\\pictures\\fekt.png')
  fekt_img = fekt_img.resize((342,111), Image.ANTIALIAS)
  fekt_img = ImageTk.PhotoImage(fekt_img)
  fekt_label = ttk.Label(image=fekt_img)
  fekt_label.image = fekt_img
  fekt_label.config(anchor=CENTER, background="white")
  fekt_label.pack()

  global logInImage
  logInImage = PhotoImage(file=fileDirectory + '\\pictures\\login.png')
  
  logInBtn = Button(master, image=logInImage, command=logInScreen, borderwidth=0, cursor="hand2", activebackground="#fff")
  logInBtn.config(background="white")
  logInBtn.pack(pady=5)
  
  global signUpImage
  signUpImage = PhotoImage(file=fileDirectory + '\\pictures\\signup.png')
  signUpBtn = Button(master, image=signUpImage, command=signUpScreen, borderwidth=0, cursor="hand2", activebackground="#fff")
  signUpBtn.configure(background="white")  
  signUpBtn.pack(pady=5)



  #treeViewBtn = Button(master, text="TreeView", font="Helvetica", command=treeView)
  #treeViewBtn.configure(background="white")
  #treeViewBtn.pack(pady=5)

def signUpScreen():
  logger.info("Sign up chosen")
  for widget in master.winfo_children():
    widget.destroy()
  master.geometry("500x500")

  mailLbl = Label(master, text="E-mail:", font="Helvetica 14 bold", background="white")
  mailLbl.config(anchor=CENTER)
  mailLbl.pack(pady=5)

  mailEntry = Entry(master, width=30, font="Helvetica", borderwidth=2)
  mailEntry.pack(pady=5)

  passwordLbl = Label(master, text="Password:", font="Helvetica 14 bold", background="white")
  passwordLbl.config(anchor=CENTER)
  passwordLbl.pack(pady=5)

  passwordEntry = Entry(master, show="*", width=30, font="Helvetica", borderwidth=2)
  passwordEntry.pack()

  filenameLbl = Label(master, text="Filename:", font="Helvetica 14 bold", background="white")
  filenameLbl.config(anchor=CENTER)
  filenameLbl.pack(pady=5)

  filenameEntry = Entry(master, width=30, font="Helvetica", borderwidth=2)
  filenameEntry.pack()

  def addToDatabase(encryption):
    signUpMail = mailEntry.get()
    signUpPassword = passwordEntry.get()
    signUpFilename = filenameEntry.get()
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
      if encryption == "des":
        e.threeDesEncrypt(signUpFilename, signUpPassword)
      elif encryption == "chacha":
        e.chaChaEncrypt(signUpFilename, signUpPassword)
      elif encryption == "aes128":
        e.aes128Encrypt(signUpFilename, signUpPassword)
      elif encryption == "aes256":
        e.aes256Encrypt(signUpFilename, signUpPassword)
    except sqlite3.IntegrityError:
      logger.info("Unsuccessful sign up with mail " + signUpMail)
      warningLabel = Label(master, text="E-mail sa už používa.", font="Helvetica", background="white")
      warningLabel.config(anchor=CENTER)
      warningLabel.pack(pady=5)

  def printDatabase():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    for row in c.execute('SELECT * FROM users;'):
      print(row)

  chooseEncryptionLbl = Label(text="Zvoľ šifrovací algoritmus a dĺžku \nkľúča na ukončenie registrácie:", font="Helvetica 12", background="white")
  chooseEncryptionLbl.config(anchor=CENTER)
  chooseEncryptionLbl.pack(pady=5)

  e = Encryption()
  desButton = Button(text="3DES", command=lambda: addToDatabase("des")).pack(pady=5)
  chaChaButton = Button(text="CaCha20", command=lambda: addToDatabase("chacha")).pack(pady=5)
  aes128Button = Button(text="AES 128bit", command=lambda: addToDatabase("aes128")).pack(pady=5)
  aes256Button = Button(text="AES 256bit", command=lambda: addToDatabase("aes256")).pack(pady=5)

  """global submitImage
  submitImage = PhotoImage(file=fileDirectory + '\\pictures\\submit.png')
  submitButton = Button(master, image=submitImage, command=lambda: addToDatabase("des"), borderwidth=0, cursor="hand2", activebackground="#fff", background="white").pack(pady=5)"""

  funButton = Button(master, text="Print Database", font="Helvetica", command=printDatabase, borderwidth=1).pack(pady=5)

  global backImage
  backImage = PhotoImage(file=fileDirectory + '\\pictures\\back.png')
  backButton = Button(master, image=backImage, command=firstScreen, cursor="hand2", borderwidth=0, background="white", activebackground="#fff").pack(pady=5)

def treeViewDatabase(filename):
  for widget in master.winfo_children():
    widget.destroy()
  master.geometry("550x600")
  master.title("Vault")
  master.resizable(False, True)
  master.iconbitmap(fileDirectory + "\\pictures\\unlocked_lock.ico")

  tree = treeViewDB()
  tree.viewFromDatabase(master, filename)
  global saveEncryptImage
  saveEncryptImage = PhotoImage(file=fileDirectory + '\\pictures\\saveencrypt.png')
  save_encrypt_button = Button(master, image=saveEncryptImage, cursor="hand2", borderwidth=0, background="white", activebackground="#fff", command=firstScreen)
  save_encrypt_button.pack(pady=5)

def logInScreen():
  logger.info("Log in chosen")

  for widget in master.winfo_children():
    widget.destroy()
  master.geometry("500x500")

  mailLbl = Label(master, text="E-mail:", font="Helvetica 14 bold")
  mailLbl.config(anchor=CENTER, background="white")
  mailLbl.pack(pady=5)

  mailEntry = Entry(master, width=30, font="Helvetica", borderwidth=2)
  mailEntry.pack(pady=5)

  passwordLbl = Label(master, text="Password:", font="Helvetica 14 bold")
  passwordLbl.config(anchor=CENTER, background="white")
  passwordLbl.pack(pady=5)

  passwordEntry = Entry(master, show="*", width=30, font="Helvetica", borderwidth=2)
  passwordEntry.pack()

  def comparePasswords():
    global mail
    mail = mailEntry.get()
    global password
    password = passwordEntry.get()
    global db
    db = Database(mail, password)
    if (db.comparePasswords() == True):
      logger.info("Log in successful as " + mail)
      global se
      se = sendEmail()
      se.send_email(mail)
      twoFactorPopUp()
    else:
      logger.info("Log in unsuccessful as " + mail)
      popUp()

  global submitImage
  submitImage = PhotoImage(file=fileDirectory + '\\pictures\\submit.png')

  submitButton = Button(master, image=submitImage, command=comparePasswords, cursor="hand2", borderwidth=0, background="white", activebackground="#fff").pack(pady=5)
  #submitButton = Button(master, text="Submit", font="Helvetica", command=comparePasswords).pack(pady=5)

  global backImage
  backImage = PhotoImage(file=fileDirectory + '\\pictures\\back.png')
  backButton = Button(master, image=backImage, command=firstScreen, cursor="hand2", borderwidth=0, background="white", activebackground="#fff").pack(pady=5)
  #backButton = Button(master, text="Back", font="Helvetica", command=firstScreen).pack(pady=5)

def popUp():
  popUpWindow = Toplevel(master)
  popUpWindow.geometry("250x50")
  popUpWindow.title("Warning")
  popUpWindow.resizable(False, False)
  popUpWindow.config(background="white")
  popUpWindow.iconbitmap(fileDirectory + "\\pictures\\warning.ico")
  warningLbl = Label(popUpWindow, text="NESPRÁVNE HESLO", font="Helvetica 10")
  warningLbl.config(anchor=CENTER, background="white")
  warningLbl.pack(pady=5)

def twoFactorPopUp():
  for widget in master.winfo_children():
    widget.destroy()
  master.geometry("500x500")

  verificationLbl = Label(master, text="Zadaj kód z mailu:", font="Helvetica 14 bold", background="white")
  verificationLbl.config(anchor=CENTER)
  verificationLbl.pack(pady=5)

  codeEntry = Entry(master, width=30, font="Helvetica", borderwidth=2)
  codeEntry.pack(pady=5)

  def codeVerification():
    if codeEntry.get() == se.getMessage():
      print(db.findFile(mail))
      print(db.findEncryption(mail))
      e = Encryption()
      if db.findEncryption(mail) == 'des':
        e.threeDesDecrypt(db.findFile(mail), password)
        treeViewDatabase(db.findFile(mail))
      elif db.findEncryption(mail) == 'chacha':
        e.chaChaDecrypt(db.findFile(mail), password)
        treeViewDatabase(db.findFile(mail))
      elif db.findEncryption(mail) == 'aes128':
        e.aes128Decrypt(db.findFile(mail), password)
        treeViewDatabase(db.findFile(mail))
      elif db.findEncryption(mail) == 'aes256':
        e.aes256Decrypt(db.findFile(mail, password))
        treeViewDatabase(db.findFile(mail))
    else:
      warningLbl = Label(master, text="Nesprávny kód.", font="Helvetica")
      warningLbl.config(anchor=CENTER)
      warningLbl.pack()

  global submitImage
  submitImage = PhotoImage(file=fileDirectory + '\\pictures\\submit.png')
  okButton = Button(master, image=submitImage, command=codeVerification, borderwidth=0, cursor="hand2", activebackground="#fff", background="white").pack(pady=5)
  
def cryptChoice():
  for widget in master.winfo_children():
    widget.destroy()
  master.geometry("500x500")

  vault = PwDatabase()
  def printDatabase():
    conn = sqlite3.connect('vault.db')
    c = conn.cursor()
    for row in c.execute('SELECT * FROM vault;'):
      print(row)
    conn.close()

  def encrypt():
    def padText(file):
      while len(file)%16 != 0:
        file = file + b'0'
      return file
    cipher = AES.new('This is a key123'.encode("utf8"), AES.MODE_CBC, 'This is an IV456'.encode("utf8"))
    with open('vault.db','rb') as f:
     orig_file = f.read()
    padded_file = padText(orig_file)
    encrypted_message = cipher.encrypt(padded_file)
    with open('vault.db', 'wb') as e:
      e.write(encrypted_message)

  def decrypt():
    cipher = AES.new('This is a key123'.encode("utf8"), AES.MODE_CBC, 'This is an IV456'.encode("utf8"))
    with open('vault.db', 'rb') as e:
      encrypted_file = e.read()
    decrypted_file = cipher.decrypt(encrypted_file)
    with open('vault.db', 'wb') as e:
      e.write(decrypted_file)

  encryptButton = Button(master, text="Encrypt", font="Helvetica", command=encrypt, cursor="hand2").pack(pady=5)
  decryptButton = Button(master, text="Decrypt", font="Helvetica", command=decrypt, cursor="hand2").pack(pady=5)
  viewButton = Button(master, text="View Database", font="Helvetica", command=vault.readDatabase, cursor="hand2").pack(pady=5)

  global backImage
  backImage = PhotoImage(file=fileDirectory + '\\pictures\\back.png')
  backButton = Button(master, image=backImage, command=firstScreen, cursor="hand2", borderwidth=0, background="white", activebackground="#fff").pack(pady=5)


firstScreen()
master.mainloop()