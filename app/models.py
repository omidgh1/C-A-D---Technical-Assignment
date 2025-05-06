from sqlalchemy import Column, Integer, String, Float
from app.database import Base


class Measurement(Base):
    __tablename__ = "measurements"

    id = Column(Integer, primary_key=True, index=True)
    co2_value = Column(Float, nullable=False)
    unit = Column(String, default="ppm")
    source = Column(String, default="unknown")
    description = Column(String, nullable=True)

