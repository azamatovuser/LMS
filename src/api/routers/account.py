from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.database import get_db
from api.models.account import Token
from api.domain.account import User as UserDomain
from api.models.account import AccountRequest, LoginRequest, CodeVerification
import os

router = APIRouter(
    tags=['User']
)

@router.post("/login")
async def login(form_data: LoginRequest, db: Session = Depends(get_db)):
    domain = UserDomain(db)
    code = domain.generate_code()
    print(code)
    domain.store_code(form_data.phone_number, code)
    domain.send_sms(form_data.phone_number, code)
    return {"message": "Code was sent to your phone"}
    


@router.post("/register")
async def register(account_request: AccountRequest, db: Session = Depends(get_db)):
    domain = UserDomain(db)
    return domain.register(account_request)


@router.post("/verify-code")
async def verify_code(form_data: CodeVerification, db: Session = Depends(get_db)):
    domain = UserDomain(db)
    code = domain.get_code(form_data.phone_number)
    if not code:
        raise HTTPException(status_code=404, detail="Code expired or not sent")
    if form_data.code != code:
        raise HTTPException(status_code=400, detail="Invalid code")
    access_token = domain.login_by_phone_number(form_data.phone_number)
    return Token(access_token=access_token, token_type="bearer")