from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from . import crud, schemas, scrapper
from .database import SessionLocal

router = APIRouter()
BASE_DIR = Path(__file__).resolve().parent


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _load_template(name: str) -> str:
    template_path = BASE_DIR / "templates" / name
    return template_path.read_text(encoding="utf-8")


@router.get("/", response_class=HTMLResponse)
def root():
    return HTMLResponse(content=_load_template("index.html"))


@router.get("/history", response_class=HTMLResponse)
def history_page():
    return HTMLResponse(content=_load_template("history.html"))


@router.post("/scrape/{city}")
def scrape_city(city: str, db: Session = Depends(get_db)):
    try:
        entry = scrapper.scrape_weather(city)
    except scrapper.WeatherScrapeError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    crud.create_weather(db, schemas.WeatherCreate(**entry))
    return {"status": "updated", "data": entry}


@router.get("/changes/{city}")
def get_changes(city: str, db: Session = Depends(get_db)):
    city = city.strip()
    latest = crud.get_latest_weather(db, city)
    previous = crud.get_previous_weather(db, city)
    if latest and previous:
        return {
            "city": city,
            "previous": {"temp": previous.temperature, "humidity": previous.humidity},
            "current": {"temp": latest.temperature, "humidity": latest.humidity},
            "difference": {
                "temp_change": latest.temperature - previous.temperature,
                "humidity_change": latest.humidity - previous.humidity,
            },
        }
    return {"message": "Not enough data yet"}


@router.get("/history-data/{city}")
def get_city_history(city: str, db: Session = Depends(get_db)):
    city = city.strip()
    if not city:
        raise HTTPException(status_code=400, detail="City name is required")

    history_rows = crud.get_weather_history(db, city)
    history = []
    previous = None

    for row in history_rows:
        change = {
            "temperature_change": 0.0,
            "humidity_change": 0.0,
        }
        if previous is not None:
            change = {
                "temperature_change": row.temperature - previous.temperature,
                "humidity_change": row.humidity - previous.humidity,
            }

        history.append(
            {
                "id": row.id,
                "city": row.city,
                "temperature": row.temperature,
                "humidity": row.humidity,
                "updated_at": row.updated_at.isoformat() if row.updated_at else None,
                "change": change,
            }
        )
        previous = row

    return {"city": city, "history": history}
