from pydantic import BaseModel, EmailStr, validator
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: EmailStr
    password: str
    is_admin: bool = False
    
    @validator('email')
    def validate_email_format(cls, v):
        if v and (not v.endswith('.com') or '@' not in v):
            raise ValueError('Email must contain "@" and end with ".com"')
        return v

class UserCreate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_admin: Optional[bool] = False
    
    @validator('email')
    def validate_email_format(cls, v):
        if v and (not v.endswith('.com') or '@' not in v):
            raise ValueError('Email must contain "@" and end with ".com"')
        return v

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_admin: Optional[bool] = None
    
    @validator('email')
    def validate_email_format(cls, v):
        if v and (not v.endswith('.com') or '@' not in v):
            raise ValueError('Email must contain "@" and end with ".com"')
        return v

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_admin: bool

    class Config:
        from_attributes = True

class AdminBase(BaseModel):
    username: str
    email: EmailStr
    password: str
    
    @validator('email')
    def validate_email_format(cls, v):
        if v and (not v.endswith('.com') or '@' not in v):
            raise ValueError('Email must contain "@" and end with ".com"')
        return v

class AdminCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class AdminLogin(BaseModel):
    username: str
    password: str

class AdminResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_super_admin: bool

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str = None

