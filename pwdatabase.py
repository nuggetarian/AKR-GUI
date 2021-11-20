import sqlite3

class PwDatabase:

  mail = ""
  password = ""
  service = ""

  def createTable(self):
    conn = sqlite3.connect('vault.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS vault (
                  service text,
                  mail text,
                  password text
                  )""")
    conn.close()

  def addValues(self, service, mail, password):
    conn = sqlite3.connect('vault.db')
    c = conn.cursor()
    c.execute("""INSERT INTO vault ('service', 'mail', 'password') VALUES (?, ?, ?);""", (service, mail, password))
    conn.commit()    
    conn.close()
  
  def readDatabase(self):
    conn = sqlite3.connect('vault.db')
    c = conn.cursor()
    for row in c.execute('SELECT * FROM vault;'):
      print(row)
    conn.close()
    