from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from apscheduler.schedulers.background import BackgroundScheduler
from .database import SessionLocal, engine
from . import models, crud, schemas, scrapper

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def run_weather_job():
    db = SessionLocal()
    try:
        entry = scrapper.scrape_weather("Chennai")
        crud.create_weather(db, schemas.WeatherCreate(**entry))
        print(f"Weather updated: {entry}")
    finally:
        db.close()

scheduler = BackgroundScheduler()
scheduler.add_job(run_weather_job, "cron", minute=0)
scheduler.start()

@app.post("/scrape/{city}")
def scrape_city(city: str, db: Session = Depends(get_db)):
    entry = scrapper.scrape_weather(city)
    crud.create_weather(db, schemas.WeatherCreate(**entry))
    return {"status": "updated", "data": entry}

@app.get("/changes/{city}")
def get_changes(city: str, db: Session = Depends(get_db)):
    latest = crud.get_latest_weather(db, city)
    previous = crud.get_previous_weather(db, city)
    if latest and previous:
        return {
            "city": city,
            "previous": {"temp": previous.temperature, "humidity": previous.humidity},
            "current": {"temp": latest.temperature, "humidity": latest.humidity},
            "difference": {
                "temp_change": latest.temperature - previous.temperature,
                "humidity_change": latest.humidity - previous.humidity
            }
        }
    return {"message": "Not enough data yet"}
