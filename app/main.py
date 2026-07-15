from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from apscheduler.schedulers.background import BackgroundScheduler

from . import models, scrapper
from .database import engine
from .routes import router

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
app.include_router(router)


def run_weather_job():
    from . import crud, schemas
    from .database import SessionLocal

    db = SessionLocal()
    try:
        entry = scrapper.scrape_weather("Chennai")
        crud.create_weather(db, schemas.WeatherCreate(**entry))
        print(f"Weather updated: {entry}")
    except scrapper.WeatherScrapeError as exc:
        print(f"Weather update failed: {exc}")
    finally:
        db.close()


scheduler = BackgroundScheduler()
scheduler.add_job(run_weather_job, "cron", minute=0)
scheduler.start()
