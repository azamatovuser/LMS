from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated
from api.database import get_db
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from api.models.account import Token
from api.domain.account import Account as AccountDomain
from api.models.account import AccountRequest
import os

router = APIRouter(
    tags=['Account']
)

@router.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    domain = AccountDomain(db)
    access_token = domain.login(form_data)
    return Token(access_token=access_token, token_type="bearer")


@router.post("/register")
async def register(account_request: AccountRequest, db: Session = Depends(get_db)):
    domain = AccountDomain(db)
    return domain.register(account_request)