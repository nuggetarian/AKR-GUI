import hashlib

class CheckSum:

    def get_checksum(self, filename):

        with open(filename + ".db", "rb") as f:
            bytes = f.read()  # read file as bytes
        
        readable_hash = hashlib.sha256(bytes).hexdigest()
        return readable_hash



"""chSum = CheckSum()
hashTab = hashSelectsql()
p = "chacha"

# v pe je uložené chacha a v hashTab.selectMail je uložené chacha z SQL tabulky -->
# --> pozri hashSelectsql tam je na to kod
# chceckSum jeten ček je funkčný a nám bude nahradene hashTab.select mail


if p == hashTab.selectMail:
    print("INTEGRITY IS OK")
else:
    print("WARNING - FILE WAS CHANGED!!!")"""