from pydantic import BaseModel, EmailStr
from datetime import datetime
from app.models.dataTypes import UserType, PackageType

class OrganizationCreate(BaseModel):
    email: EmailStr
    password: str
    name: str
    package_type: PackageType = PackageType.basic

class OrganizationResponse(BaseModel):
    id: int
    email: EmailStr
    type: UserType
    name: str
    package_type: PackageType
    created_at: datetime
    access_token: str
    refresh_token: str

    class Config:
        from_attributes = True
