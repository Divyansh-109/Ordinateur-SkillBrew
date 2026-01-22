class Email:
    def __init__(self, mail):
        self.mail = mail
    
    def validate(self):
        if "@" not in self.mail or "." not in self.mail.split("@")[-1]:
            raise ValueError("Invalid email address")
        return True
    
    def get_domain(self):
        return self.mail.split("@")[-1]
    
email = input("Enter your email address: ")
user_email = Email(email)
try:
    if user_email.validate():
        print(f"Email is valid. Domain: {user_email.get_domain()}")
except ValueError as e:
    print(e)

