import sqlite3
import bcrypt

class Database:

  mail = ""
  password = ""
  """conn = sqlite3.connect('users.db')
  c = conn.cursor()"""
  hashed = ""

  def __init__(self, mail, password):
    self.mail = mail
    self.password = password
    self.hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

  def createTable(self):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (
                  mail text,
                  password text
                  )""")
    conn.close()

  def addValues(self):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("""INSERT INTO users ('mail', 'password') VALUES (?, ?);""", (self.mail, self.hashed))
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

    