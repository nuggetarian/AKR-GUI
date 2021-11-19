import string    
import random  

class RandomCode:

    def random_code(self):
        self.char_number = 5  #dĺžka náhodne generovaného kódu
        self.ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = self.char_number))    
        #print("Your SECURITY CODE is : " + str(self.ran)) # vypíše nahodný kód   
        return self.ran  