import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from RandomCode import RandomCode

class sendEmail:
    
    rn = RandomCode()
    code = rn.random_code()
    

    def send_email(self, recipient): # Funkcia na odoslanie mailu s kodom
        # Udaje uctu ktory odosiela overovaci mail
        self.gmailUser = 'adventurousmanager@gmail.com'
        self.gmailPassword = '8^Tfj3@RGL'
        self.recipient = recipient
        
        # Obsah spravy
        message = str("YOUR SECURITY CODE IS: " + self.code)

        msg = MIMEMultipart()
        msg['From'] = f'"AdventurousManager" <{self.gmailUser}>'
        msg['To'] = self.recipient
        msg['Subject'] = "VERIFICATION CODE"
        msg.attach(MIMEText(message))

        # Samotne odosielanie, pouziva sa kniznica email.mime a smtplib
        try:
            mailServer = smtplib.SMTP('smtp.gmail.com', 587)
            mailServer.ehlo()
            mailServer.starttls()
            mailServer.ehlo()
            mailServer.login(self.gmailUser, self.gmailPassword)
            mailServer.sendmail(self.gmailUser, self.recipient, msg.as_string())
            mailServer.close()
            print ('Email sent!')
        except:
            print ('Something went wrong...')

    def getMessage(self): # Getter pre kod ktory bol odoslany
        return str(self.code)