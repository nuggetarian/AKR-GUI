from tkinter import *
from tkinter import ttk
from tkinter import font
import sqlite3
from pwdatabase import PwDatabase
import os

from pwdatabase import PwDatabase

class treeViewDB():
    def viewFromDatabase(self, master, filename):

      absolutepath = os.path.abspath(__file__)
      fileDirectory = os.path.dirname(absolutepath) 

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
      tree_frame = Frame(master)
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
          conn = sqlite3.connect(filename + '.db')
          c = conn.cursor()
          try:
            c.execute("INSERT INTO vault VALUES (:id, :service, :username, :password)",
                      {
                        'id': id_entry.get().strip(),
                        'service': service_entry.get(),
                        'username': username_entry.get(),
                        'password': password_entry.get()
                      })
            conn.commit()
          except sqlite3.IntegrityError:
            warningLbl = Label(master, text="Id nebolo zadané, alebo už existuje.", font="Helvetica", background="white")
            warningLbl.config(anchor=CENTER)
            warningLbl.pack()
          clearBoxes()
          conn.close()

          my_tree.delete(*my_tree.get_children())
          readDatabase()

      def readDatabase():
          conn = sqlite3.connect(filename + '.db')
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
            conn = sqlite3.connect(filename + '.db')
            c = conn.cursor()
            c.execute("DELETE FROM vault WHERE oid=" + id_entry.get())
            conn.commit()

            clearBoxes()
            conn.close()		
          except:  
            warningLbl = Label(master, text="Nič nebolo zvolené.", font="Helvetica", background="white")
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
          try:
            id_entry.insert(0, values[0])
            service_entry.insert(0, values[1])
            username_entry.insert(0, values[2]) 
            password_entry.insert(0, values[3])
          except:
            print("Click.")

      # Boxes
      data_frame = LabelFrame(master, text="Data", background="white", font="Helvetica")
      data_frame.pack(fill="x", expand="yes", padx=20)

      id_label = Label(data_frame, text="ID", background="white", font="Helvetica")
      id_label.grid(row=0, column=0, padx=10, pady=10)
      id_entry = Entry(data_frame, borderwidth=2)
      id_entry.grid(row=0, column=1, padx=10, pady=10)

      service_label = Label(data_frame, text="Service", background="white", font="Helvetica")
      service_label.grid(row=0, column=2, padx=10, pady=10)
      service_entry = Entry(data_frame, borderwidth=2)
      service_entry.grid(row=0, column=3, padx=10, pady=10)

      username_label = Label(data_frame, text="Username", background="white", font="Helvetica")
      username_label.grid(row=1, column=0, padx=10, pady=10)
      username_entry = Entry(data_frame, borderwidth=2)
      username_entry.grid(row=1, column=1, padx=10, pady=10)

      password_label = Label(data_frame, text="Password", background="white", font="Helvetica")
      password_label.grid(row=1, column=2, padx=10, pady=10)
      password_entry = Entry(data_frame, borderwidth=2)
      password_entry.grid(row=1, column=3, padx=10, pady=10)

      # Add Buttons
      button_frame = LabelFrame(master, borderwidth=0, background="white")
      button_frame.pack(padx=10)

      global addImage
      addImage = PhotoImage(file=fileDirectory + '\\pictures\\add.png')

      add_button = Button(button_frame, image=addImage, cursor="hand2", borderwidth=0, command=addToDatabase, background="white", activebackground="#fff")
      add_button.grid(row=0, column=0, padx=10, pady=10)

      global removeImage
      removeImage = PhotoImage(file=fileDirectory + '\\pictures\\remove.png')

      remove_one_button = Button(button_frame, image=removeImage, command=removeFromDatabase, cursor="hand2", borderwidth=0, background="white", activebackground="#fff")
      remove_one_button.grid(row=0, column=1 ,padx=10, pady=10)


      my_tree.bind("<ButtonRelease-1>", select_record)

      readDatabase()