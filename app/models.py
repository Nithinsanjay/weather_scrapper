from sqlalchemy import Column, Integer, Float, String, DateTime
from datetime import datetime
from .database import Base

class WeatherData(Base):
    __tablename__ = "weather_data"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, index=True)
    temperature = Column(Float)
    humidity = Column(Float)
    updated_at = Column(DateTime, default=datetime.utcnow)
