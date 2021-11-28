import hashlib

class CheckSum:

    def get_checksum(self, filename):

        with open(filename + ".db", "rb") as f:
            bytes = f.read()  # Precitanie suboru ako bajty
        
        readable_hash = hashlib.sha256(bytes).hexdigest() # Hash zo suboru
        return readable_hash