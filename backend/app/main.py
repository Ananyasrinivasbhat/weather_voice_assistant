from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.nlp import process_text  # Import the NLP function
from app.search import get_weather, get_current_location, get_recent_searches  # Import functions
from app.current import get_current_location_weather  # Import the current location weather function

import logging
from datetime import datetime
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Allow your frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB setup
mongodb_uri = os.getenv("MONGODB_URI")
client = MongoClient(mongodb_uri)
db = client["voice_assistant"]
interactions = db["interactions"]

# Define request model
class UserQuery(BaseModel):
    text: str

class LocationQuery(BaseModel):
    lat: float
    lon: float

@app.post("/process")
async def process_query(query: UserQuery, request: Request):
    try:
        # Log incoming request
        payload = await request.json()
        logger.debug(f"Incoming request payload: {payload}")

        # Process the query with NLP
        nlp_result = process_text(query.text)
        logger.debug(f"NLP result: {nlp_result}")

        # Handle the "Bengaluru" case separately
        if query.text.lower() == "bengaluru":
            weather_data = get_current_location_weather("Bengaluru")
            log_entry = {
                "query": query.text,
                "city": "Bengaluru",
                "response": weather_data,
                "timestamp": datetime.now(),
            }
            interactions.insert_one(log_entry)
            return {"intent": "get_weather", "city": "Bengaluru", "weather": weather_data}

        # Handle other intents
        if nlp_result["intent"] == "get_recent_searches":
            recent_searches = get_recent_searches()
            return {"intent": "get_recent_searches", "recent_searches": recent_searches}

        elif nlp_result["intent"] == "get_weather":
            city = nlp_result.get("city")
            if not city:
                city = get_current_location()
                if not city:
                    return {"intent": "unknown", "message": "Could not determine location"}

            weather_data = get_weather(city)

            log_entry = {
                "query": query.text,
                "city": city,
                "response": weather_data,
                "timestamp": datetime.now(),
            }
            interactions.insert_one(log_entry)

            return {"intent": "get_weather", "city": city, "weather": weather_data}

        else:
            return nlp_result

    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/current-location-weather")
async def current_location_weather(query: LocationQuery):
    try:
        # Fetch weather data for the current location (Bengaluru for now)
        weather_data = get_current_location_weather("Bengaluru")

        # Log interaction to MongoDB
        log_entry = {
            "query": "Current location weather for Bengaluru",
            "response": weather_data,
            "timestamp": datetime.now(),
        }
        interactions.insert_one(log_entry)

        return weather_data
    except Exception as e:
        logger.error(f"Error fetching current location weather: {e}")
        raise HTTPException(status_code=500, detail=str(e))