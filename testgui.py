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
from Crypto.Cipher import AES
from treeview import treeViewDB

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

def treeViewDatabase():

  for widget in master.winfo_children():
    widget.destroy()
  master.geometry("550x600")
  master.title("Vault")
  master.iconbitmap(fileDirectory + "\\pictures\\unlocked_lock.ico")

  tree = treeViewDB()
  tree.viewFromDatabase(master)
  global saveEncryptImage
  saveEncryptImage = PhotoImage(file=fileDirectory + '\\pictures\\saveencrypt.png')
  save_encrypt_button = Button(master, image=saveEncryptImage, cursor="hand2", borderwidth=0, background="white", activebackground="#fff", command=firstScreen)
  save_encrypt_button.pack(pady=5)

def treeView():
    # Add Some Style
    style = ttk.Style()

    # Pick A Theme
    style.theme_use("clam")

    # Configure the Treeview Colors
    style.configure("Treeview", 
                    background="#fff",
                    foreground="black",
                    rowheight=25,
                    fieldbackground="#fff")

    # Change Selected Color
    style.map('Treeview',
              background=[('selected', "#c22740")])

    # Create a Treeview Frame
    tree_frame = Frame(root)
    tree_frame.pack(pady=10)

    # Create a Treeview Scrollbar
    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)

    # Create The Treeview
    my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
    my_tree.pack()

    # Configure the Scrollbar
    tree_scroll.config(command=my_tree.yview)

    # Define Our Columns
    my_tree['columns'] = ("ID", "Service", "Username", "Password")

    # Format Our Columns
    my_tree.column("#0", width=0, stretch = NO)
    my_tree.column("ID", anchor=W, width=70)
    my_tree.column("Service", anchor=W, width=140)
    my_tree.column("Username", anchor=W, width=140)
    my_tree.column("Password", anchor=W, width=100)

    # Create Headings
    my_tree.heading("#0", text="", anchor=W)
    my_tree.heading("ID", text="ID", anchor=W)
    my_tree.heading("Service", text="Service", anchor=W)
    my_tree.heading("Username", text="Username", anchor=W)
    my_tree.heading("Password", text="Password", anchor=W)


    # Ceate Striped Row Tags
    my_tree.tag_configure('oddrow', background="white")
    my_tree.tag_configure('evenrow', background="#f78396")

    # Functions
    def addToDatabase():
        conn = sqlite3.connect('vault.db')
        c = conn.cursor()
        c.execute("INSERT INTO vault VALUES (:id, :user, :service, :password)",
                  {
                    'id': id_entry.get(),
                    'user': username_entry.get(),
                    'service': service_entry.get(),
                    'password': password_entry.get()
                  })
        conn.commit()
        clearBoxes()
        conn.close()

        my_tree.delete(*my_tree.get_children())
        readDatabase()

    def readDatabase():
        conn = sqlite3.connect('vault.db')
        c = conn.cursor()
        c.execute("SELECT * FROM vault")
        records = c.fetchall()
        global count
        count = 0
        for record in records:
          if count % 2 == 0:
            my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3]), tags=('evenrow',))
          else:
            my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3]), tags=('oddrow',))
          # Increment Counter
          count += 1
        conn.close()

    def clearBoxes():
      id_entry.delete(0, END)
      username_entry.delete(0, END)
      service_entry.delete(0, END)
      password_entry.delete(0, END)

    def removeFromDatabase():
        try:
          x = my_tree.selection()[0]
          my_tree.delete(x)
          conn = sqlite3.connect('vault.db')
          c = conn.cursor()
          c.execute("DELETE FROM vault WHERE oid=" + id_entry.get())
          conn.commit()

          clearBoxes()
          conn.close()		
        except:  
          warningLbl = Label(root, text="Nič nebolo zvolené.", font="Helvetica")
          warningLbl.pack(pady=5)
            
    def select_record(e):
        # Clear entry boxes
        service_entry.delete(0, END)
        username_entry.delete(0, END)
        id_entry.delete(0, END)
        password_entry.delete(0, END)

        # Grab record Number
        selected = my_tree.focus()
        # Grab record vales
        values = my_tree.item(selected, 'values')

        # outputs to entry boxes
        service_entry.insert(0, values[1])
        username_entry.insert(0, values[2])
        id_entry.insert(0, values[0])
        password_entry.insert(0, values[3])

    # Boxes
    data_frame = LabelFrame(root, text="Data")
    data_frame.pack(fill="x", expand="yes", padx=20)

    service_label = Label(data_frame, text="Service")
    service_label.grid(row=0, column=2, padx=10, pady=10)
    service_entry = Entry(data_frame)
    service_entry.grid(row=0, column=3, padx=10, pady=10)

    username_label = Label(data_frame, text="Username")
    username_label.grid(row=1, column=0, padx=10, pady=10)
    username_entry = Entry(data_frame)
    username_entry.grid(row=1, column=1, padx=10, pady=10)

    password_label = Label(data_frame, text="Password")
    password_label.grid(row=1, column=2, padx=10, pady=10)
    password_entry = Entry(data_frame)
    password_entry.grid(row=1, column=3, padx=10, pady=10)

    id_label = Label(data_frame, text="ID")
    id_label.grid(row=0, column=0, padx=10, pady=10)
    id_entry = Entry(data_frame)
    id_entry.grid(row=0, column=1, padx=10, pady=10)


    # Add Buttons
    button_frame = LabelFrame(root, borderwidth=0)
    button_frame.pack(padx=10)

    global addImage
    addImage = PhotoImage(file='add.png')

    add_button = Button(button_frame, image=addImage, cursor="hand2", borderwidth=0, command=addToDatabase)
    add_button.grid(row=0, column=0, padx=10, pady=10)

    global removeImage
    removeImage = PhotoImage(file='remove.png')

    remove_one_button = Button(button_frame, image=removeImage, command=removeFromDatabase, cursor="hand2", borderwidth=0)
    remove_one_button.grid(row=0, column=1 ,padx=10, pady=10)

    global saveEncryptImage
    saveEncryptImage = PhotoImage(file='saveencrypt.png')
    save_encrypt_button = Button(root, image=saveEncryptImage, cursor="hand2", borderwidth=0)
    save_encrypt_button.pack(pady=5)


    my_tree.bind("<ButtonRelease-1>", select_record)

    pwdb = PwDatabase()
    pwdb.createTable()
    readDatabase()

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
      treeViewDatabase()
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