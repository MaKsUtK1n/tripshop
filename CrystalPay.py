from requests import get, post




url = "https://api.crystalpay.io/v3/"
class CrystalPay:

    def __init__(self, auth_login: str, auth_secret: str) -> None:
        self.login = auth_login
        self.secret = auth_secret
    
    def getBalances(self, hide_empty: bool = True):
        res = post(f"{url}balance/list/", json={'hide_empty': hide_empty, "auth_login": self.login, "auth_secret": self.secret})
        return res.json()
    
    def createInvoice(self, amount: float, lifetime: float = 10, currency: str = "USD", redirect_url: str = "https://t.me", extra: str = ""):
        res = post(f"{url}invoice/create/", json={"auth_login": self.login, "auth_secret": self.secret, "amount": amount, "type": "purchase", "lifetime": lifetime, "amount_currency": currency, "redirect_url": redirect_url, "extra": extra})
        return res.json()
    
    def getInvoice(self, invoice_id: str):
        res = post(f"{url}invoice/info/", json={"auth_login": self.login, "auth_secret": self.secret, "id": invoice_id})
        return res.json()








if __name__ == "__main__":
    CP = CrystalPay("penes", "e574ecf7b448e04bee21c54e98b1c61f7818e953")
    print(CP.getInvoice("715320106_WNThknPBtveUkp"))