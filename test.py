from encryption import Encryption

e = Encryption()

file = input("File:")
password = input("Password:")

#e.threeDesEncrypt(file, password)
#e.threeDesDecrypt(file, password)
e.aes128Decrypt(file, password)
