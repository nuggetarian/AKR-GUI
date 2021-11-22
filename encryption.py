from Crypto.Cipher import AES
from pwdatabase import PwDatabase


pwdb = PwDatabase()
"""pwdb.createTable()"""

# ADD DATA
"""pwdb.addValues("Facebook", "kontrafakt@gmail.com", "test123")
pwdb.addValues("Twitter", "kontrafakt@gmail.com", "bruh123")
pwdb.addValues("YouTube", "kontrafakt@gmail.com", "haha134")"""

# DISPLAY FILE
pwdb.readDatabase()

# ENCRYPT DATABASE
"""def padText(file):
  while len(file)%16 != 0:
    file = file + b'0'
  return file

cipher = AES.new('This is a key123'.encode("utf8"), AES.MODE_CBC, 'This is an IV456'.encode("utf8"))

with open('vault.db','rb') as f:
  orig_file = f.read()

padded_file = padText(orig_file)

encrypted_message = cipher.encrypt(padded_file)

with open('vault.db', 'wb') as e:
  e.write(encrypted_message)"""


# DISPLAY FILE
#pwdb.readDatabase()


# DECRYPT DATABASE

"""cipher = AES.new('This is a key123'.encode("utf8"), AES.MODE_CBC, 'This is an IV456'.encode("utf8"))

with open('vault.db', 'rb') as e:
  encrypted_file = e.read()

decrypted_file = cipher.decrypt(encrypted_file)

with open('vault.db', 'wb') as e:
  e.write(decrypted_file)"""


# DISPLAY FILE
"""pwdb.readDatabase()"""


"""def padText(plain_text):
  while len(plain_text)%16 != 0:
    plain_text = plain_text + " "
  return plain_text

obj = AES.new('This is a key123'.encode("utf8"), AES.MODE_CBC, 'This is an IV456'.encode("utf8"))
plain_text = "A really secret message. Not for prying eyes."
cipher_text = obj.encrypt(padText(plain_text).encode("utf8"))
print(cipher_text)

obj2 = AES.new('This is a key123'.encode("utf8"), AES.MODE_CBC, 'This is an IV456'.encode("utf8"))
decrypted = obj2.decrypt(cipher_text.rstrip())
print(decrypted)"""





# ENCRYPT FILE
"""def padText(file):
  while len(file)%16 != 0:
    file = file + b'0'
  return file

cipher = AES.new('This is a key123'.encode("utf8"), AES.MODE_CBC, 'This is an IV456'.encode("utf8"))

with open('text.txt','rb') as f:
  orig_file = f.read()

padded_file = padText(orig_file)

encrypted_message = cipher.encrypt(padded_file)

with open('text.txt', 'wb') as e:
  e.write(encrypted_message)"""


# DECRYPT FILE

"""cipher = AES.new('This is a key123'.encode("utf8"), AES.MODE_CBC, 'This is an IV456'.encode("utf8"))

with open('text.txt', 'rb') as e:
  encrypted_file = e.read()

decrypted_file = cipher.decrypt(encrypted_file)

with open('text.txt', 'wb') as e:
  e.write(decrypted_file)"""