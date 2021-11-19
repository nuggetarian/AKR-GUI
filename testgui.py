import hashlib, sqlite3
from tkinter import *
from tkinter import ttk
from sqliteoperations import Database
import os
from sqliteoperations import Database

absolutepath = os.path.abspath(__file__)
fileDirectory = os.path.dirname(absolutepath)

master = Tk()
master.title("Password Manager")
master.iconbitmap(fileDirectory + "\\lock.ico")


def loginScreen():
  master.geometry("250x200")

  optionLbl = Label(master, text="Zvol moznost", font="Helvetica")
  optionLbl.config(anchor=CENTER)
  optionLbl.pack(pady=5)

  logInBtn = Button(master, text="Log in", font="Helvetica")
  logInBtn.pack(pady=5)
  
  signUpBtn = Button(master, text="Sign up", font="Helvetica", command=signUpScreen)
  signUpBtn.pack(pady=5)

  treeViewBtn = Button(master, text="TreeView", font="Helvetica", command=treeView)
  treeViewBtn.pack(pady=5)

def signUpScreen():
  top = Toplevel(master)
  top.geometry("250x150")
  top.iconbitmap(fileDirectory + "\\lock.ico")
  mailLbl = Label(top, text="E-mail:", font="Helvetica")
  mailLbl.config(anchor=CENTER)
  mailLbl.pack()

  mailEntry = Entry(top)
  mailEntry.pack()

  passwordLbl = Label(top, text="Password:", font="Helvetica")
  passwordLbl.config(anchor=CENTER)
  passwordLbl.pack()

  passwordEntry = Entry(top, show="*")
  passwordEntry.pack()

  def addToDatabase():
    mail = mailEntry.get()
    password = passwordEntry.get()
    db = Database(mail, password)
    db.addValues()
    top.destroy()

  """def printDatabase():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    for row in c.execute('SELECT * FROM users;'):
      print(row)"""

  submitButton = Button(top, text="Submit", font="Helvetica", command=addToDatabase).pack(pady=5)
  #funButton = Button(top, text="Print Database", font="Helvetica", command=printDatabase).pack(pady=5)

def treeView():
    treeWindow = Toplevel(master)
    treeWindow.geometry("500x500")
    my_tree = ttk.Treeview(treeWindow)

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

loginScreen()
master.mainloop()

