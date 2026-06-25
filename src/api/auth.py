from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.models.database import get_db
from src.models.entities import User, UserRole
from src.middleware.security import get_password_hash, verify_password, create_access_token
from src.middleware.dependencies import get_current_user
from src.schemas.response import APIResponse, success_response, error_response
from pydantic import BaseModel, EmailStr
import uuid
import random
from datetime import datetime, timedelta

router = APIRouter()

class UserRegister(BaseModel):
    name: str
    email: EmailStr
    phone: str
    password: str
    confirm_password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class ForgotPassword(BaseModel):
    email: EmailStr

class VerifyOTP(BaseModel):
    email: EmailStr
    otp: str

class ResetPassword(BaseModel):
    email: EmailStr
    reset_token: str
    new_password: str
    confirm_new_password: str

@router.post("/register", response_model=APIResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: UserRegister, db: Session = Depends(get_db)):
    if user.password != user.confirm_password:
        return error_response("Passwords do not match")

    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        return error_response("Email already registered")
    
    hashed_pwd = get_password_hash(user.password)
    new_user = User(
        name=user.name, 
        email=user.email, 
        phone=user.phone, 
        hashed_password=hashed_pwd,
        role=UserRole.DEVOTEE
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return success_response("User registered successfully", {"user_id": new_user.id})

@router.post("/login", response_model=APIResponse)
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        return error_response("Invalid email or password")
    
    access_token = create_access_token(data={"sub": db_user.email, "role": db_user.role.value, "user_id": db_user.id})
    return success_response("Login successful", {
        "access_token": access_token, 
        "token_type": "bearer", 
        "role": db_user.role.value
    })

@router.post("/forgot-password", response_model=APIResponse)
def forgot_password(req: ForgotPassword, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == req.email).first()
    if not user:
        return error_response("Email not found")
    
    # Generate 6-digit OTP
    otp = str(random.randint(100000, 999999))
    user.reset_otp = otp
    user.otp_expiry = datetime.utcnow() + timedelta(minutes=10)
    db.commit()
    
    # In a real app, send an email/SMS with the OTP here.
    return success_response("OTP sent to your email successfully", {"mock_otp": otp})

@router.post("/verify-otp", response_model=APIResponse)
def verify_otp(req: VerifyOTP, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == req.email).first()
    if not user or user.reset_otp != req.otp:
        return error_response("Invalid OTP")
    
    if user.otp_expiry < datetime.utcnow():
        return error_response("OTP has expired")
        
    # Generate a reset token
    reset_token = str(uuid.uuid4())
    user.reset_otp = reset_token # Store token in same field for simplicity
    db.commit()
    
    return success_response("OTP verified successfully", {"reset_token": reset_token})

@router.post("/reset-password", response_model=APIResponse)
def reset_password(req: ResetPassword, db: Session = Depends(get_db)):
    if req.new_password != req.confirm_new_password:
        return error_response("New passwords do not match")
    
    user = db.query(User).filter(User.email == req.email).first()
    if not user or user.reset_otp != req.reset_token:
        return error_response("Invalid or expired reset token")
    
    user.hashed_password = get_password_hash(req.new_password)
    user.reset_otp = None
    user.otp_expiry = None
    db.commit()
    
    return success_response("Password has been reset successfully")

@router.get("/profile", response_model=APIResponse)
def get_user_profile(current_user: User = Depends(get_current_user)):
    return success_response("Profile fetched", {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "phone": current_user.phone,
        "role": current_user.role.value
    })
