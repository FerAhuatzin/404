from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from app.models.base import Base
from app.models.dataTypes import UserType, user_type_enum

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    type = Column(user_type_enum, default=UserType.individual, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
