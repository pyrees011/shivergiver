from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from bson import ObjectId


# Mock database
class MockDB:
    appointments = []


db = MockDB()


class Appointment(BaseModel):
    title: str
    date: datetime
    time: str
    duration: int
    participants: List[ObjectId]
    status: str = "scheduled"


app = FastAPI()


# Create a new appointment
@app.post("/appointments/")
async def create_appointment(appointment: Appointment):
    appointment_dict = appointment.dict()
    db.appointments.append(appointment_dict)
    return {"message": "Appointment created successfully"}


# Retrieve all appointments
@app.get("/appointments/")
async def get_all_appointments():
    return db.appointments


# Retrieve an appointment by ID
@app.get("/appointments/{appointment_id}")
async def get_appointment_by_id(appointment_id: int):
    for appointment in db.appointments:
        if appointment["_id"] == appointment_id:
            return appointment
    raise HTTPException(status_code=404, detail="Appointment not found")


# Update an appointment by ID
@app.put("/appointments/{appointment_id}")
async def update_appointment(appointment_id: int, appointment: Appointment):
    for i, a in enumerate(db.appointments):
        if a["_id"] == appointment_id:
            db.appointments[i] = appointment.dict()
            return {"message": "Appointment updated successfully"}
    raise HTTPException(status_code=404, detail="Appointment not found")


# Delete an appointment by ID
@app.delete("/appointments/{appointment_id}")
async def delete_appointment(appointment_id: int):
    for i, appointment in enumerate(db.appointments):
        if appointment["_id"] == appointment_id:
            del db.appointments[i]
            return {"message": "Appointment deleted successfully"}
    raise HTTPException(status_code=404, detail="Appointment not found")
