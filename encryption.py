from Crypto.Cipher import DES3
from Crypto.Cipher import ChaCha20
from Crypto.Cipher import AES
from hashlib import md5
from pwdatabase import PwDatabase


class Encryption:

  def threeDes168Encrypt(self, filename, password):
    # Precitanie suboru
    with open(filename + '.db', 'rb') as input_file:
      file_bytes = input_file.read()
    # Sifrovanie
    password.encode('utf8')


    def keyGen(key):
            while len(key) % 21 != 0:
                key = key + '0'
            return key
    # Generování klíče
    key_hash = md5(keyGen(password).encode('utf8')).digest()
    
    tdes_key = DES3.adjust_key_parity(key_hash)
    cipher = DES3.new(tdes_key, DES3.MODE_EAX, nonce=b'0') 
    new_file_bytes = cipher.encrypt(file_bytes)
    # Zapis zasifrovaneho obsahu do suboru
    with open(filename + '.db', 'wb') as output:
      output.write(new_file_bytes)

  def threeDes168Decrypt(self, filename, password):
    with open(filename + '.db', 'rb') as input_file:
      file_bytes = input_file.read()

    def keyGen(key):
            while len(key) % 21 != 0:
                key = key + '0'
            return key
    # Generování klíče
    key_hash = md5(keyGen(password).encode('utf8')).digest()
    tdes_key = DES3.adjust_key_parity(key_hash)
    cipher = DES3.new(tdes_key, DES3.MODE_EAX, nonce=b'0')  
    
    new_file_bytes = cipher.decrypt(file_bytes)
    with open(filename + '.db', 'wb') as output:
      output.write(new_file_bytes)

  def threeDes112Encrypt(self, filename , password):
     # Precitanie suboru
    with open(filename + '.db', 'rb') as input_file:
      file_bytes = input_file.read()
    # Sifrovanie
    password.encode('utf8')


    def keyGen(key):
            while len(key) % 14 != 0:
                key = key + '0'
            return key
    # Generování klíče
    key_hash = md5(keyGen(password).encode('utf8')).digest()
    
    tdes_key = DES3.adjust_key_parity(key_hash)
    cipher = DES3.new(tdes_key, DES3.MODE_EAX, nonce=b'0') 
    new_file_bytes = cipher.encrypt(file_bytes)
    # Zapis zasifrovaneho obsahu do suboru
    with open(filename + '.db', 'wb') as output:
      output.write(new_file_bytes)  
            
  def threeDes112Decrypt(self, filename, password):
    with open(filename + '.db', 'rb') as input_file:
      file_bytes = input_file.read()

    def keyGen(key):
            while len(key) % 14 != 0:
                key = key + '0'
            return key
    # Generování klíče
    key_hash = md5(keyGen(password).encode('utf8')).digest()
    tdes_key = DES3.adjust_key_parity(key_hash)
    cipher = DES3.new(tdes_key, DES3.MODE_EAX, nonce=b'0')  
    
    new_file_bytes = cipher.decrypt(file_bytes)
    with open(filename + '.db', 'wb') as output:
      output.write(new_file_bytes)

  def chaChaEncrypt(self, filename, password):
    def keyGen(key):
            while len(key) % 32 != 0:
                key = key + b'0'
            return key
    # Generování klíče
    key = keyGen(bytes(password, 'utf-8'))

    # Načtení databáze do proměnné
    with open(filename + '.db', 'rb') as input_file:
        file_bytes = input_file.read()
    input_file.close()

    plaintext = file_bytes
    cipher = ChaCha20.new(key=key)
    ciphertext = cipher.encrypt(plaintext)
    nonce = cipher.nonce

    with open(filename + '.db', 'wb') as output:
      output.write(ciphertext)
    with open(filename + '_nonce.txt', 'wb') as nonc:
      nonc.write(nonce)

    output.close()
    nonc.close()

  def chaChaDecrypt(self, filename, password):
    def keyGen(key):
            while len(key) % 32 != 0:
                key = key + b'0'
            return key
    # Generování klíče
    key = keyGen(bytes(password, 'utf-8'))

    # Načtení databáze do proměnné
    with open(filename + '.db', 'rb') as input_file:
        file_bytes = input_file.read()
    input_file.close()

    try:
      with open(filename + '_nonce.txt', 'rb') as nc:
        nonce = nc.read()
      with open(filename + '.db', 'rb')as ciphtext:
        ciphertext = ciphtext.read()

      cipher = ChaCha20.new(key=key, nonce=nonce)
      dectext = cipher.decrypt(ciphertext)

      with open(filename + '.db', 'wb') as dec:
        dec.write(dectext)

      nc.close()
      ciphtext.close()
      dec.close()
    except ValueError or KeyError:
      print("Incorrect decryption")

  def aes128Encrypt(self, filename, password):

    def keyGen(key):
      while len(key) % 16 != 0:
          key = key + b'0'
      return key
    key = keyGen(bytes(password, 'utf-8'))
    iv = "This is an IV456"

    cipher = AES.new(key, AES.MODE_CBC, bytes(iv, 'utf-8'))
    with open(filename + '.db', 'rb') as f:
      message = f.read()

    ciphertext = cipher.encrypt(message)

    with open(filename + '.db', 'wb') as e:
      e.write(ciphertext)

  def aes128Decrypt(self, filename, password):

    def keyGen(key):
      while len(key) % 16 != 0:
          key = key + b'0'
      return key
    key = keyGen(bytes(password, 'utf-8'))
    iv = "This is an IV456"

    cipher = AES.new(key, AES.MODE_CBC, bytes(iv, 'utf-8'))
    with open(filename + '.db', 'rb') as f:
      message = f.read()

    ciphertext = cipher.decrypt(message)

    with open(filename + '.db', 'wb') as e:
      e.write(ciphertext)

  def aes256Encrypt(self, filename, password):

    def keyGen(key):
      while len(key) % 32 != 0:
          key = key + b'0'
      return key
    key = keyGen(bytes(password, 'utf-8'))
    iv = "This is an IV456"

    cipher = AES.new(key, AES.MODE_CBC, bytes(iv, 'utf-8'))
    with open(filename + '.db', 'rb') as f:
      message = f.read()

    ciphertext = cipher.encrypt(message)

    with open(filename + '.db', 'wb') as e:
      e.write(ciphertext)

  def aes256Decrypt(self, filename, password):

    def keyGen(key):
      while len(key) % 32 != 0:
          key = key + b'0'
      return key
    key = keyGen(bytes(password, 'utf-8'))
    iv = "This is an IV456"

    cipher = AES.new(key, AES.MODE_CBC, bytes(iv, 'utf-8'))
    with open(filename + '.db', 'rb') as f:
      message = f.read()

    ciphertext = cipher.decrypt(message)

    with open(filename + '.db', 'wb') as e:
      e.write(ciphertext)






























































































































"""pwdb = PwDatabase()"""
"""pwdb.createTable()"""

# ADD DATA
"""pwdb.addValues("Facebook", "kontrafakt@gmail.com", "test123")
pwdb.addValues("Twitter", "kontrafakt@gmail.com", "bruh123")
pwdb.addValues("YouTube", "kontrafakt@gmail.com", "haha134")"""

# DISPLAY FILE
"""pwdb.readDatabase()"""

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