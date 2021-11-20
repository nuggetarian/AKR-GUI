import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import font
from types import CellType
from pwdatabase import PwDatabase
from sqliteoperations import Database
import os
import logging
from PIL import ImageTk, Image
from email_pokus import sendEmail

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

#NIEČO SPRAVIŤ BIELE = xxxx.configure(background="white")

def firstScreen():
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

  def addToDatabase():
    mail = mailEntry.get()
    password = passwordEntry.get()
    db = Database(mail, password)
    db.createTable()
    try:
      db.addValues()
      firstScreen()
      success = Label(master, text="Registrácia prebehla úspešne.", font="Helvetica", background="white")
      logger.info("User signed up with mail " + mail)
      success.config(anchor=CENTER)
      success.pack(pady = 5)
    except sqlite3.IntegrityError:
      logger.info("Unsuccessful sign up with mail " + mail)
      warningLabel = Label(master, text="E-mail sa už používa.", font="Helvetica", background="white")
      warningLabel.config(anchor=CENTER)
      warningLabel.pack(pady=5)

  def printDatabase():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    for row in c.execute('SELECT * FROM users;'):
      print(row)

  global submitImage
  submitImage = PhotoImage(file=fileDirectory + '\\pictures\\submit.png')
  submitButton = Button(master, image=submitImage, command=addToDatabase, borderwidth=0, cursor="hand2", activebackground="#fff", background="white").pack(pady=5)

  funButton = Button(master, text="Print Database", font="Helvetica", command=printDatabase, borderwidth=1).pack(pady=5)

  global backImage
  backImage = PhotoImage(file=fileDirectory + '\\pictures\\back.png')
  backButton = Button(master, image=backImage, command=firstScreen, cursor="hand2", borderwidth=0, background="white", activebackground="#fff").pack(pady=5)

def treeView():
    for widget in master.winfo_children():
      widget.destroy()
    master.geometry("500x500")
    """treeWindow = Toplevel(master)
    treeWindow.geometry("450x250")"""
    my_tree = ttk.Treeview(master)

    my_tree['columns'] = ("Service", "E-mail", "Password")

    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("Service", anchor=W, width=120, minwidth=20)
    my_tree.column("E-mail", anchor=W, width=120, minwidth=20)
    my_tree.column("Password", anchor=W, width=120, minwidth=20)

    my_tree.heading("#0", text="", anchor=W)
    my_tree.heading("Service", text="Service", anchor=W)
    my_tree.heading("E-mail", text="E-mail", anchor=W)
    my_tree.heading("Password", text="Password", anchor=W)

    """my_tree.insert(parent='', index='end', iid=0, text="", values=("Facebook", "kontrafakt@gmail.com", "bozknarozlucku"))
    my_tree.insert(parent='', index='end', iid=1, text="", values=("YouTube", "kontrafakt@gmail.com", "ego"))
    my_tree.insert(parent='', index='end', iid=2, text="", values=("Github", "kontrafakt@gmail.com", "anys"))"""

    data=[
      ["Facebook", "kontrafakt@gmail.com", "bozknarozlucku"],
      ["YouTube", "kontrafakt@gmail.com", "ego"],
      ["Github", "kontrafakt@gmail.com", "anys"]
    ]
    count=0
    for record in data:
      my_tree.insert(parent='', index='end', iid=count, text="", values=(record[0], record[1], record[2]))
      count += 1
    

    my_tree.pack(pady=20)

def logInScreen():
  logger.info("Log in chosen")
  pwdb = PwDatabase()
  pwdb.createTable()

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
    mail = mailEntry.get()
    password = passwordEntry.get()
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
      #PLACEHOLDER
      treeView()
    else:
      warningLbl = Label(master, text="Nesprávny kód.", font="Helvetica")
      warningLbl.config(anchor=CENTER)
      warningLbl.pack()

  global submitImage
  submitImage = PhotoImage(file=fileDirectory + '\\pictures\\submit.png')
  okButton = Button(master, image=submitImage, command=codeVerification, borderwidth=0, cursor="hand2", activebackground="#fff", background="white").pack(pady=5)
  

firstScreen()
master.mainloop()

