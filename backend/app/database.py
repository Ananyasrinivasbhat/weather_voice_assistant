from pymongo import MongoClient
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Check if the environment variable is loaded
mongodb_uri = os.getenv("MONGODB_URI")
if not mongodb_uri:
    raise ValueError("MONGODB_URI not found in .env file")

# Connect to MongoDB
try:
    client = MongoClient(mongodb_uri)
    db = client["voice_assistant"]
    interactions = db["interactions"]
    print("Connected to MongoDB successfully!")
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")
    raise

def log_interaction(query: str, response: dict):
    """
    Log user interactions with additional metadata.
    """
    log_entry = {
        "query": query,
        "response": response,
        "timestamp": datetime.now(),
        "metadata": {
            "intent": response.get("intent", "unknown"),
            "entities": response.get("entities", []),
            "sentiment": response.get("sentiment", {}),
        }
    }
    try:
        interactions.insert_one(log_entry)
        print("Interaction logged successfully!")
    except Exception as e:
        print(f"Failed to log interaction: {e}")
        raise