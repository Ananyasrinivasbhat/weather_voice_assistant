import os
import requests
from fastapi import HTTPException # type: ignore
import logging

# Configure logging
logger = logging.getLogger(__name__)

def get_current_location_weather(city: str = "Bengaluru"):
    """
    Fetch weather data for a specific city (default: Bengaluru).
    """
    try:
        api_key = os.getenv("OPENWEATHER_API_KEY")
        if not api_key:
            logger.error("OpenWeather API key not found")
            raise HTTPException(status_code=500, detail="OpenWeather API key not found")

        # Fetch weather data for the specified city
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        return {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "condition": data["weather"][0]["description"],
        }
    except requests.exceptions.HTTPError as e:
        logger.error(f"Failed to fetch weather data: {e}")
        raise HTTPException(status_code=404, detail=f"Weather data not found for {city}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch weather data: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch weather data: {e}")