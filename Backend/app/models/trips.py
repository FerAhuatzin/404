from sqlalchemy import Column, Integer, ForeignKey, Float, DateTime
from geoalchemy2 import Geography
from app.models.base import Base

class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True))
    start_location = Column(Geography(geometry_type='POINT', srid=4326), nullable=False)
    end_location = Column(Geography(geometry_type='POINT', srid=4326))
    distance_meters = Column(Float, default=0)
    duration_seconds = Column(Float, default=0)
    carbon_saved_grams = Column(Float, default=0)
