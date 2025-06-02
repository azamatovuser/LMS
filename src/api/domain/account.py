from passlib.context import CryptContext
from datetime import timedelta, datetime, timezone
from api.crud.account import Account as AccountCrud
from fastapi import HTTPException, status
from passlib.hash import django_pbkdf2_sha256
import os
import jwt

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
pwd_context = CryptContext(
    schemes=["pbkdf2_sha256", "argon2", "bcrypt", "bcrypt_sha256"],
    deprecated="auto"
)

class Account:
    def __init__(self, db):
        self.crud = AccountCrud(db)

    def login(self, form_data):
        self.crud.get_all_accounts()
        user = self.authenticate_account(form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=1260)
        access_token = self.create_access_token(
            data={"sub": user.username, "user_id": user.id}, expires_delta=access_token_expires
        )
        return access_token

    def get_password_hash(self, password):
        return pwd_context.hash(password)
    
    def verify_password(self, plain_password, hashed_password):
        try:
            return pwd_context.verify(plain_password, hashed_password)        
        except Exception:
            return django_pbkdf2_sha256.verify(plain_password, hashed_password)

    
    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    def authenticate_account(self, username: str, password: str):
        account = self.crud.get_account(username)
        if not account:
            return False
        if not self.verify_password(password, account.password):
            return False
        return account
    
    def register(self, account_request):
        if account_request.password != account_request.confirm_password:
            return HTTPException(status_code=400, detail="Passwords do not match")
        user = self.crud.get_account(account_request.username)
        if user:
            return HTTPException(status_code=400, detail="Username already exists")
        
        password = self.get_password_hash(account_request.password)
        self.crud.register(account_request, password)
        return HTTPException(status_code=200, detail="Registration went successfully")
    
