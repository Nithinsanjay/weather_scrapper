import requests
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY")
WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather"


class WeatherScrapeError(Exception):
    pass

def scrape_weather(city: str):
    city = city.strip()
    if not city:
        raise WeatherScrapeError("City name is required")
    if not API_KEY:
        raise WeatherScrapeError("WEATHER_API_KEY is not configured")

    response = requests.get(
        WEATHER_URL,
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
        "updated_at": datetime.utcnow()
    }
