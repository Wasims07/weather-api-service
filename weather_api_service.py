from fastapi import FastAPI, HTTPException, Request, Depends, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import os
import time
import logging
import httpx
import asyncio

# Configuration
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
WEATHERAPI_KEY = os.getenv("WEATHERAPI_KEY", "")
CACHE_TTL = int(os.getenv("CACHE_TTL", 300))
RATE_LIMIT_PER_MIN = int(os.getenv("RATE_LIMIT_PER_MIN", 60))

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("weather_service")

# FastAPI Instance
app = FastAPI(title="Weather API Service", version="1.0")

# Models
class WeatherCurrent(BaseModel):
    location: str
    provider: str
    temperature_c: float
    feels_like_c: Optional[float]
    condition: Optional[str]

class ForecastDay(BaseModel):
    date: str
    temp_min_c: float
    temp_max_c: float
    condition: Optional[str]

class ForecastResponse(BaseModel):
    location: str
    provider: str
    days: List[ForecastDay]

class LocationResult(BaseModel):
    name: str
    lat: float
    lon: float
    country: Optional[str]

# Simple in-memory cache
class TTLCache:
    def __init__(self, ttl_seconds: int):
        self.ttl = ttl_seconds
        self.store = {}
        self.lock = asyncio.Lock()

    async def get(self, key):
        async with self.lock:
            entry = self.store.get(key)
            if entry and time.time() - entry["ts"] < self.ttl:
                return entry["value"]
            self.store.pop(key, None)
            return None

    async def set(self, key, value):
        async with self.lock:
            self.store[key] = {"value": value, "ts": time.time()}

cache = TTLCache(CACHE_TTL)

# Endpoints
@app.get("/")
async def root():
    return {"message": "Weather API Service is running!"}

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/weather/current", response_model=WeatherCurrent)
async def current_weather(location: str = Query(...)):
    return WeatherCurrent(location=location, provider="dummy", temperature_c=25.0, feels_like_c=24.0, condition="Sunny")

@app.get("/weather/forecast", response_model=ForecastResponse)
async def forecast_weather(location: str = Query(...), days: int = Query(3)):
    forecast_days = [ForecastDay(date=f"2025-09-{26+i}", temp_min_c=20+i, temp_max_c=30+i, condition="Sunny") for i in range(days)]
    return ForecastResponse(location=location, provider="dummy", days=forecast_days)

@app.get("/locations/search", response_model=List[LocationResult])
async def locations_search(q: str = Query(...)):
    return [LocationResult(name=q, lat=0.0, lon=0.0, country="Nowhere")]

# Run
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("weather_api_service:app", host="127.0.0.1", port=8000, reload=True)