from sqlalchemy import Column, Integer, String, func, DateTime, Boolean, Enum
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field
from api.database import Base
from sqlalchemy import Enum as SqlEnum
from enum import Enum

class Status(str, Enum):
    free = 'free'
    premium = 'premium'

class Role(str, Enum):
    admin = 'admin'
    student = 'student'

class Account(Base):
    __tablename__ = "account_account"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(SqlEnum(Status, name="status_enum"), nullable=False, default=Status.free)
    role = Column(SqlEnum(Role, name="role_enum"), nullable=False, default=Role.student)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    username = Column(String, unique=True)
    email = Column(String, nullable=False)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    is_staff = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    date_joined = Column(DateTime, default=func.now())
    created_date = Column(DateTime, default=func.now())

class Token(BaseModel):
    access_token: str
    token_type: str


class AccountRequest(BaseModel):
    first_name: str = Field(min_length=3)
    last_name: str = Field(min_length=3)
    username: str = Field(min_length=3)
    phone_number: str = Field(min_length=3)
    email: str = Field(min_length=3)
    password: str = Field(min_length=6)
    confirm_password: str = Field(min_length=6)

class LoginRequest(BaseModel):
    phone_number: str
    password: str

class CodeVerification(BaseModel):
    phone_number: str
    code: str