from pydantic import BaseModel
from datetime import datetime

class WeatherBase(BaseModel):
    city: str
    temperature: float
    humidity: float

class WeatherCreate(WeatherBase):
    pass

class WeatherOut(WeatherBase):
    updated_at: datetime

    class Config:
        orm_mode = True
