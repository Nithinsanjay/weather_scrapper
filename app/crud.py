from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models, schemas

def create_weather(db: Session, entry: schemas.WeatherCreate):
    db_entry = models.WeatherData(**entry.model_dump())
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

def get_latest_weather(db: Session, city: str):
    return (
        db.query(models.WeatherData)
        .filter(func.lower(models.WeatherData.city) == city.lower())
        .order_by(models.WeatherData.updated_at.desc())
        .first()
    )

def get_previous_weather(db: Session, city: str):
    return (
        db.query(models.WeatherData)
        .filter(func.lower(models.WeatherData.city) == city.lower())
        .order_by(models.WeatherData.updated_at.desc())
        .offset(1)
        .first()
    )
