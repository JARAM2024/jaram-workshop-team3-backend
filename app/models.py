from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class SensorData(Base):
    __tablename__ = "sensor_data"
    id = Column(Integer, primary_key=True, index=True)
    temperature = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
    is_raining = Column(Boolean, default=False)
    umbrella_present = Column(Boolean, default=False)
    door_open = Column(Boolean, default=False)
