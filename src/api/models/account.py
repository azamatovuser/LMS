from sqlalchemy import Column, Integer, String, func, DateTime, Boolean, Enum, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field
from api.database import Base
from sqlalchemy import Enum as SqlEnum
from enum import Enum
from datetime import datetime

class Status(str, Enum):
    free = 'free'
    premium = 'premium'

class Role(str, Enum):
    admin = 'admin'
    student = 'student'

class SubscriptionType(str, Enum):
    free = "free"
    premium = "premium"

class User(Base):
    __tablename__ = "account_user"

    id = Column(Integer, primary_key=True, index=True)
    role = Column(SqlEnum(Role, name="role_enum"), nullable=False, default=Role.student)
    phone_number = Column(String, nullable=False)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    is_staff = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    created_date = Column(DateTime, default=func.now())

    subscription = relationship("Subscription", back_populates="user", uselist=False)

class Subscription(Base):
    __tablename__ = "account_subscription"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("account_user.id"), unique=True)
    type = Column(SqlEnum(SubscriptionType, name="subscription_type_enum"), nullable=False, default=SubscriptionType.free)
    start_date = Column(DateTime, default=func.now())
    end_date = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    created_date = Column(DateTime, default=func.now())

    user = relationship("User", back_populates="subscription")

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