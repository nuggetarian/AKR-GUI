import string    
import random  

class RandomCode:

    def random_code(self): # Funkcia na generovanie nahodneho kodu
        self.char_number = 5  # Dlzka nahodne generovaneho kodu
        self.ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = self.char_number))      
        return self.ran  