# weather-api-service
A FastAPI-based Weather API Service with endpoints for current weather, forecasts, and location search. Includes in-memory caching, basic health checks, and ready-to-use API documentation.

## Features
- Get current weather for a location
- Get weather forecast for multiple days
- Search locations by query
- Health check endpoint
- Built-in caching to reduce API calls
- Interactive API docs via Swagger UI

## Installation

1. **Clone the repository** (optional if using Git):
```bash
git clone https://github.com/Wasims07/weather-api-service.git
cd weather-api-service
```

## Running the API
```bash
uvicorn weather_api_service:app --reload
```

## API Endpoints
```bash
GET /weather/current?location={city} → Get current weather
GET /weather/forecast?location={city}&days={n} → Get forecast
GET /locations/search?q={query} → Search for locations
GET /health → Health check
```

## Approach

The Weather API Service is built using FastAPI, designed to be lightweight, fast, and easy to extend. The main approach includes:

- Modular API Endpoints – Separate endpoints for current weather, forecasts, location search, and health checks.
- Caching – In-memory TTL cache to reduce repeated API calls and improve response times.
- Error Handling & Logging – Robust error handling with clear logging for easier debugging.
- External API Integration – Aggregates data from multiple weather providers (OpenWeatherMap, WeatherAPI) for reliability.
- Interactive Documentation – Automatically generated Swagger UI for testing and exploring endpoints.

This design ensures scalability, maintainability, and quick local testing while keeping the service production-ready.
