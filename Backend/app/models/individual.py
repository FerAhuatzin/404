from sqlalchemy import Column, String, Integer, ForeignKey, Float
from app.models.base import Base

class Individual(Base):
    __tablename__ = "individuals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    full_name = Column(String, nullable=False)
    total_carbon_reduction_grams = Column(Float, default=0.0)
    total_points = Column(Integer, default=0)
    points_balance = Column(Integer, default=0)
    carbon_credits_balance = Column(Float, default=0.0)