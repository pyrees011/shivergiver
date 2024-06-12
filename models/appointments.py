from pydantic import BaseModel, Field, ValidationError
from datetime import date
from bson import ObjectId
from typing import List

class AppointmentModel(BaseModel):
    title: str
    date: str
    time: str
    duration: int
    participants: List[str]
    status: str = Field(..., description="Status of the appointment")

    STATUS_OPTIONS: List = ["scheduled", "cancelled", "completed"]

    class Config:
        schema_extra = {
            "example": {
                "title": "Meeting",
                "date": "2024-06-15",
                "time": "14:00",
                "duration": 60,
                "participants": [
                    "610a4f22d53aa2d7a5e41ae0",
                    "610a4f22d53aa2d7a5e41ae1",
                ],
                "status": "scheduled",
            }
        }
