from pydantic import BaseModel, Field
from datetime import datetime
from typing import List
from bson import ObjectId


class AppointmentModel(BaseModel):
    title: str
    date: datetime
    time: str
    duration: int
    participants: List[ObjectId]

    STATUS_OPTIONS = ["scheduled", "completed", "canceled", "rescheduled"]
    status: str = Field(
        ..., description="Status of the appointment", enum=STATUS_OPTIONS
    )

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
