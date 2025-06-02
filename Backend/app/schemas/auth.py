from pydantic import BaseModel, EmailStr
from app.models.dataTypes import UserType

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class RefreshTokenResponse(BaseModel):
    access_token: str
    refresh_token: str 

class UserInfoResponse(BaseModel):
    id: int
    email: EmailStr
    type: UserType
    refresh_token: str    
    access_token: str
