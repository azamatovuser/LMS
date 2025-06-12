from api.models.account import User as UserDB

class User:
    def __init__(self, db):
        self.db = db

    def get_account_by_phone(self, phone_number):
        return self.db.query(UserDB).filter(UserDB.phone_number == phone_number).first()

    def register(self, account_request, password):
        new_account = UserDB(
            username=account_request.username,
            first_name=account_request.first_name,
            last_name=account_request.last_name,
            phone_number=account_request.phone_number,
            email=account_request.email,
            password=password,
        )
        self.db.add(new_account)
        self.db.commit()