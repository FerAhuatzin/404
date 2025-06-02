from sqlalchemy import Column, String, Integer, ForeignKey, Enum
from app.models.base import Base
from app.models.dataTypes import PackageType
class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    package_type = Column(Enum(PackageType), default=PackageType.basic)
