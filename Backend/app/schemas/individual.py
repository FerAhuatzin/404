from pydantic import BaseModel, EmailStr, constr
from datetime import datetime
from app.models.dataTypes import UserType

class IndividualUserCreate(BaseModel):
    email: EmailStr
    password: constr(min_length=8)
    full_name: constr(min_length=2)

class IndividualUserResponse(BaseModel):
    id: int
    email: str
    type: UserType
    full_name: str
    created_at: datetime
    access_token: str
    refresh_token: str

    class Config:
        from_attributes = True 

class GoogleUserInfo(BaseModel):
    email: str
    name: str
    picture: str | None = None
