from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["your_database"]  # Replace 'your_database' with your actual database name

# Define the appointment collection
appointment_collection = db["appointments"]

# Define the schema
appointment_schema = {
    "title": {"type": "string", "required": True},
    "date": {"type": "date", "required": True},
    "time": {"type": "string", "required": True},
    "duration": {"type": "number", "required": True},  # duration in minutes
    "participants": {"type": "array", "items": {"type": "objectid", "ref": "users"}},
    "status": {
        "type": "string",
        "enum": ["scheduled", "completed", "canceled"],
        "default": "scheduled",
    },
}


# Insert a new appointment
def insert_appointment(appointment_data):
    appointment_collection.insert_one(appointment_data)


# Example usage:
new_appointment = {
    "title": "Meeting",
    "date": datetime(2024, 6, 10),
    "time": "09:00",
    "duration": 60,
    "participants": [ObjectId("participant_id_1"), ObjectId("participant_id_2")],
    "status": "scheduled",
}

insert_appointment(new_appointment)
