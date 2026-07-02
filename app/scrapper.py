import requests
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY")

def scrape_weather(city: str):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url).json()
    return {
        "city": city,
        "temperature": response["main"]["temp"],
        "humidity": response["main"]["humidity"],
        "updated_at": datetime.utcnow()
    }
