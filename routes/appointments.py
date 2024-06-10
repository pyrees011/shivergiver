from fastapi import APIRouter, Body, HTTPException
from models.appointment import AppointmentModel
from config.mongo import db
from bson import ObjectId

router = APIRouter()
appointment_collection = db.appointments


@router.post("/appointments", tags=["appointments"])
async def create_appointment(appointment: AppointmentModel = Body(...)):
    new_appointment = appointment_collection.appointments.insert_one(appointment.dict())
    created_appointment = appointment_collection.appointments.find_one(
        {"_id": new_appointment.inserted_id}
    )
    return created_appointment


@router.get("/appointments", tags=["appointments"])
async def get_all_appointments():
    appointments = appointment_collection.appointments.find()
    return [appointment for appointment in appointments]


@router.get("/appointments/{appointment_id}", tags=["appointments"])
async def get_appointment(appointment_id: str):
    appointment = appointment_collection.appointments.find_one(
        {"_id": ObjectId(appointment_id)}
    )
    if appointment:
        return appointment
    raise HTTPException(status_code=404, detail="Appointment not found")


@router.put("/appointments/{appointment_id}", tags=["appointments"])
async def update_appointment(
    appointment_id: str, appointment: AppointmentModel = Body(...)
):
    updated_appointment = appointment_collection.appointments.find_one_and_update(
        {"_id": ObjectId(appointment_id)},
        {"$set": appointment.dict()},
        return_document=True,
    )
    if updated_appointment:
        return updated_appointment
    raise HTTPException(status_code=404, detail="Appointment not found")


@router.delete("/appointments/{appointment_id}", tags=["appointments"])
async def delete_appointment(appointment_id: str):
    deleted_appointment = appointment_collection.appointments.find_one_and_delete(
        {"_id": ObjectId(appointment_id)}
    )
    if deleted_appointment:
        return {"message": "Appointment deleted successfully"}
    raise HTTPException(status_code=404, detail="Appointment not found")
