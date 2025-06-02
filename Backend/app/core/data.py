from pydantic import BaseModel
from app.models.dataTypes import UserType

class TokenInformation(BaseModel):
    id: int
    type: UserType
    token_type: str = "access"

class RefreshTokenInformation(BaseModel):
    id: int
    type: UserType
    token_type: str = "refresh"
