import sqlite3

class PwDatabase:

  mail = ""
  password = ""
  service = ""

  def createTable(self, filename): # Vytvorenie databazy s heslami, na zaklade uzivatelovho nazvu
    conn = sqlite3.connect(filename + '.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS vault (
                  id integer not null primary key,
                  service text,
                  mail text,
                  password text
                  )""")
    conn.close()

  
    