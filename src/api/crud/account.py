from api.models.account import Account as AccountDB

class Account:
    def __init__(self, db):
        self.db = db

    def get_account(self, username: str):
        account = self.db.query(AccountDB).filter(username==AccountDB.username).first()
        return account
    
    def get_all_accounts(self):
        print(self.db.query(AccountDB).all())

    def register(self, account_request, password):
        new_account = AccountDB(
            username=account_request.username,
            first_name=account_request.first_name,
            last_name=account_request.last_name,
            phone_number=account_request.phone_number,
            email=account_request.email,
            password=password,
        )
        self.db.add(new_account)
        self.db.commit()