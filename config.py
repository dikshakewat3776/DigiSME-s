from intuitlib.enums import Scopes

__env__ = "sandbox"   # "production"

if __env__ == "sandbox":
    class Config:
        class Intuit:
            CLIENT_ID = "ABxIxSlfNGyaR4AEMXyVwuHQxCa9QH0gKdwisMVj8zmMLIROJb"
            CLIENT_SECRET = "QwzxqcRflJrvjofb96BUoAU0ITqbAxjuejTl5gV2"
            ENVIRONMENT = __env__
            REDIRECT_URI = "https://localhost:5000/callback"

            BASE_URL = "https://sandbox-quickbooks.api.intuit.com"

            scopes = [
                Scopes.ACCOUNTING,
                Scopes.PAYMENT,
            ]
else:
    class Config:
        class Intuit:
            CLIENT_ID = ""
            CLIENT_SECRET = ""
            ENVIRONMENT = __env__
            REDIRECT_URI = ""

            BASE_URL = ""

            scopes = [
                Scopes.ACCOUNTING,
                Scopes.PAYMENT,
            ]
