from sqlalchemy.orm import Session
from . import models, schemas

def create_weather(db: Session, entry: schemas.WeatherCreate):
    db_entry = models.WeatherData(**entry.dict())
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

def get_latest_weather(db: Session, city: str):
    return db.query(models.WeatherData).filter_by(city=city).order_by(models.WeatherData.updated_at.desc()).first()

def get_previous_weather(db: Session, city: str):
    return db.query(models.WeatherData).filter_by(city=city).order_by(models.WeatherData.updated_at.desc()).offset(1).first()
