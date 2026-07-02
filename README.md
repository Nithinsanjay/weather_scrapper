# 🌦️ Weather Scraper API

A FastAPI backend that scrapes live weather data from OpenWeatherMap and stores it in PostgreSQL.  
It supports scheduled scraping, manual triggers, and comparison of changes between readings.

---

## 🚀 Features
- Fetch live weather data for any city using OpenWeatherMap API.
- Store results in PostgreSQL with SQLAlchemy ORM.
- Compare latest vs. previous readings (temperature & humidity).
- Automatic scheduled scraping with APScheduler.
- Interactive API docs via Swagger UI (`/docs`).

---

## 📦 Requirements
Install dependencies:
```bash
pip install -r requirements.txt
