import os
import requests
import logging
from pymongo import MongoClient
from datetime import datetime
from fastapi import HTTPException
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# MongoDB setup
mongodb_uri = os.getenv("MONGODB_URI")
client = MongoClient(mongodb_uri)
db = client["voice_assistant"]
interactions = db["interactions"]

def get_weather(city: str):
    """ Fetch weather data from OpenWeather API """
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        logger.error("OpenWeather API key not found")
        raise HTTPException(status_code=500, detail="OpenWeather API key not found")

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()
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
        raise HTTPException(status_code=404, detail=f"City '{city}' not found")
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch weather data: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch weather data: {e}")

def get_current_location():
    """ Fetch user's city based on IP address """
    try:
        response = requests.get("http://ip-api.com/json/")
        data = response.json()
        return data.get("city")
    except Exception as e:
        logger.error(f"Error fetching location: {e}")
        return None

def get_recent_searches():
    """ Retrieve recent search queries from MongoDB """
    try:
        return list(interactions.find({}, {"_id": 0}).sort("timestamp", -1).limit(5))
    except Exception as e:
        logger.error(f"Error fetching recent searches: {e}")
        return []
