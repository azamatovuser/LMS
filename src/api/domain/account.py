from passlib.context import CryptContext
from datetime import timedelta, datetime, timezone
from api.crud.account import User as UserCrud
from fastapi import HTTPException, status
from passlib.hash import django_pbkdf2_sha256
import os
import jwt
from random import randint
import httpx
import redis
import requests

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)
pwd_context = CryptContext(
    schemes=["pbkdf2_sha256", "argon2", "bcrypt", "bcrypt_sha256"],
    deprecated="auto"
)

class User:
    def __init__(self, db):
        self.crud = UserCrud(db)
        self.token = None

    def login(self, form_data):
        user = self.authenticate_account_by_phone(form_data.phone_number, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect phone number or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=1260)
        access_token = self.create_access_token(
            data={"sub": user.phone_number, "user_id": user.id}, expires_delta=access_token_expires
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
    
    def authenticate_account_by_phone(self, phone_number: str, password: str):
        account = self.crud.get_account_by_phone(phone_number)
        if not account:
            return False
        if not self.verify_password(password, account.password):
            return False
        return account
    
    def login_by_phone_number(self, phone_number: str):
        user = self.crud.get_account_by_phone(phone_number)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        access_token_expires = timedelta(minutes=1260)
        access_token = self.create_access_token(
            data={"sub": user.phone_number, "user_id": user.id},
            expires_delta=access_token_expires
        )
        return access_token
    
    def register(self, account_request):
        if account_request.password != account_request.confirm_password:
            return HTTPException(status_code=400, detail="Passwords do not match")
        user = self.crud.get_account_by_phone(account_request.phone_number)
        if user:
            return HTTPException(status_code=400, detail="User already exists")
        
        password = self.get_password_hash(account_request.password)
        self.crud.register(account_request, password)
        return HTTPException(status_code=200, detail="Registration went successfully")
    
    def generate_code(self):
        return str(randint(100000, 999999))
    
    def authenticate(self):
        response = requests.post(
            f"{os.getenv("ESKIZ_BASE_URL")}/auth/login",
            data={"email": os.getenv("ESKIZ_EMAIL"), "password": os.getenv("ESKIZ_PASSWORD")}
        )
        response.raise_for_status()
        self.token = response.json()["data"]["token"]

    def send_sms(self, phone: str, code: str):
        if self.token is None:
            self.authenticate()

        phone = phone.strip().replace("+998", "").replace("998", "")
        if not phone.isdigit() or len(phone) != 9:
            raise ValueError("Phone number must be in +998XXXXXXXXX or 998XXXXXXXXX format")

        headers = {"Authorization": f"Bearer {self.token}"}
        print(phone, code)
        data = {
            "mobile_phone": phone,
            "message": f"This is test from Eskiz",
            "from": "4546"
        }

        response = requests.post(f"{os.getenv("ESKIZ_BASE_URL")}/message/sms/send", headers=headers, data=data)

        if response.status_code == 401:
            self.authenticate()
            headers["Authorization"] = f"Bearer {self.token}"
            response = requests.post(f"{os.getenv("ESKIZ_BASE_URL")}/message/sms/send", headers=headers, data=data)

        if response.status_code != 200:
            print("Eskiz response:", response.text)

        response.raise_for_status()
        return response.json()

        
    def store_code(self, phone_number, code, expires_in=60):
        return redis_client.setex(f"verify:{phone_number}", expires_in, code)
        
    def get_code(self, phone_number):
        return redis_client.get(f"verify:{phone_number}")
