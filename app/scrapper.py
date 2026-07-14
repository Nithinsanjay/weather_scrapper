import os
from datetime import datetime

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY")
OPENWEATHER_URL = "http://api.openweathermap.org/data/2.5/weather"
GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


class WeatherScrapeError(Exception):
    pass


def _fetch_openweather(city: str):
    response = requests.get(
        OPENWEATHER_URL,
        params={"q": city, "appid": API_KEY, "units": "metric"},
        timeout=10,
    )

    try:
        data = response.json()
    except ValueError as exc:
        raise WeatherScrapeError("Weather service returned an invalid response") from exc

    if response.status_code != 200:
        message = data.get("message", "weather service error") if isinstance(data, dict) else "weather service error"
        raise WeatherScrapeError(f"OpenWeatherMap error: {message}")

    main = data.get("main")
    if not isinstance(main, dict):
        raise WeatherScrapeError("Weather service response did not include weather data")

    return {
        "city": data.get("name", city),
        "temperature": main["temp"],
        "humidity": main["humidity"],
        "updated_at": datetime.utcnow(),
    }


def _fetch_open_meteo(city: str):
    geocode_response = requests.get(
        GEOCODE_URL,
        params={"name": city, "count": 1, "language": "en", "format": "json"},
        timeout=10,
    )
    geocode_response.raise_for_status()
    geocode_data = geocode_response.json()
    results = geocode_data.get("results") or []
    if not results:
        raise WeatherScrapeError("City not found")

    location = results[0]
    forecast_response = requests.get(
        FORECAST_URL,
        params={
            "latitude": location.get("latitude"),
            "longitude": location.get("longitude"),
            "current": "temperature_2m,relative_humidity_2m",
            "timezone": "auto",
        },
        timeout=10,
    )
    forecast_response.raise_for_status()
    forecast_data = forecast_response.json()
    current = forecast_data.get("current") or {}

    return {
        "city": location.get("name", city),
        "temperature": current.get("temperature_2m"),
        "humidity": current.get("relative_humidity_2m"),
        "updated_at": datetime.utcnow(),
    }


def scrape_weather(city: str):
    city = city.strip()
    if not city:
        raise WeatherScrapeError("City name is required")

    try:
        if API_KEY:
            return _fetch_openweather(city)
        return _fetch_open_meteo(city)
    except requests.RequestException as exc:
        raise WeatherScrapeError("Weather service is currently unavailable") from exc
