from sqlalchemy import Column, String, Integer, ForeignKey, Float
from app.models.base import Base

class AuthToken(Base):
    __tablename__ = "authTokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token = Column(String, nullable=False)
    refresh_token = Column(String, nullable=False)