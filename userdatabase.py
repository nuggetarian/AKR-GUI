import sqlite3
import bcrypt

class Database:

  mail = ""
  password = ""
  hashed = ""
  #filename = ""

  def __init__(self, mail, password):
    self.mail = mail
    self.password = password
    self.hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

  def createTable(self):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    c.execute("""CREATE TABLE IF NOT EXISTS users (
                  mail TEXT NOT NULL UNIQUE,
                  password TEXT NOT NULL,
                  filename TEXT NOT NULL,
                  encryption TEXT NOT NULL
                  )""")
    conn.close()

  def addValues(self, filename, encryption):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("""INSERT INTO users ('mail', 'password', 'filename', 'encryption') VALUES (?, ?, ?, ?);""", (self.mail, self.hashed, filename, encryption))
    conn.commit()    
    conn.close()
  
  def comparePasswords(self):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE mail=:mail", {'mail': self.mail})
    hashed = c.fetchall()
    result = hashed[0][0]
    conn.close()
    if bcrypt.checkpw(self.password.encode(), result):
      return True
    else:
      return False

  def findFile(self, mail):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT filename FROM users WHERE mail=:mail", {'mail': mail})
    hashed = c.fetchall()
    result = hashed[0][0]
    conn.close()
    return result

  def findEncryption(self, mail):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT encryption FROM users WHERE mail=:mail", {'mail': mail})
    hashed = c.fetchall()
    result = hashed[0][0]
    conn.close()
    return result

    