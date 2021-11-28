import sqlite3
import bcrypt
from checksum import CheckSum

class Database:

  mail = ""
  password = ""
  hashed = ""
  #filename = ""

  def __init__(self, mail, password): # Konstruktor
    self.mail = mail
    self.password = password
    self.hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()) # Heslo je zahashovane cez kniznicu bcrypt

  def createTable(self): # Vytvorenie databazy s uzivatelmi
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    c.execute("""CREATE TABLE IF NOT EXISTS users (
                  mail TEXT NOT NULL UNIQUE,
                  password TEXT NOT NULL,
                  filename TEXT NOT NULL,
                  encryption TEXT NOT NULL,
                  checksum TEXT
                  )""")
    conn.close()

  def addValues(self, filename, encryption): # Pridanie hodnot do tabulky
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("""INSERT INTO users ('mail', 'password', 'filename', 'encryption') VALUES (?, ?, ?, ?);""", (self.mail, self.hashed, filename, encryption))
    conn.commit()    
    conn.close()
  
  def comparePasswords(self): # Porovnanie hesla ktore sme zadali s heslom ktore mame v databaze, pouzivame bcrypt
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

  def findFile(self, mail): # Funkcia na najdenie suboru na zaklade mailu, ktory uzivatel pouzil pri vytvarani
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT filename FROM users WHERE mail=:mail", {'mail': mail})
    hashed = c.fetchall()
    result = hashed[0][0]
    conn.close()
    return result

  def findEncryption(self, mail): # Funkcia na najdenie aky sifrovaci algoritmus uzivatel zvolil
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT encryption FROM users WHERE mail=:mail", {'mail': mail})
    hashed = c.fetchall()
    result = hashed[0][0]
    conn.close()
    return result

  def findChecksum(self, filename): # Funkcia na najdenie checksumu ktory vznikol ked uzivatel ulozil subor
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT checksum FROM users WHERE filename=:filename", {'filename': filename})
    hashed = c.fetchall()
    result = hashed[0][0]
    conn.close()
    return result

  def addChecksumValues(self, filename): # Funkcia na pridanie checksumu do databazy ked uzivatel ulozil subor
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    checksum = CheckSum()
    c.execute("""UPDATE users SET checksum=? WHERE filename=?;""", (checksum.get_checksum(filename), filename))
    conn.commit()    
    conn.close()


    