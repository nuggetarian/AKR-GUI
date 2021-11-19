import hashlib, sqlite3
from tkinter import *
from sqliteoperations import Database

master = Tk()

master.title("Password Vault")

def startScreen():
  master.geometry("250x200")
  lbl = Label(master, text="Vyber moznost")
  lbl.config(anchor=CENTER)
  lbl.pack()

  btn = Button(master, text="Prihlasit sa", command=quit).pack(pady=5)

  def signUp():
    signUpWindow = Toplevel(master)
    signUpWindow.title("Sign Up")
    # sets the geometry of toplevel
    signUpWindow.geometry("250x200")
    # A Label widget to show in toplevel
    lbl2 = Label(signUpWindow, text ="E-mail").pack()
    
    txt = Entry(signUpWindow, width=20)
    txt.pack()
    txt.focus()
    mail = txt.get()

    lbl2 = Label(signUpWindow, text ="Password").pack()
    txt = Entry(signUpWindow, width=20, show="*")
    txt.pack()
    password = txt.get()
    btnPrintStuff = Button(signUpWindow, text= "Sign Up", command=print("bruh"))
    btnPrintStuff.pack(pady=5)

    """database = Database(mail, password)
    database.addValues()"""

  btn1 = Button(master, text="Registrovat sa", command=signUp).pack(pady=5)

  btn2 = Button(master, text="Exit", command=quit).pack(pady=5)



startScreen()
mainloop()
"""master.mainloop()"""