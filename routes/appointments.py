from fastapi import APIRouter, Body, HTTPException, Depends
from models.appointments import AppointmentModel
from config.mongo_config import db
from bson import ObjectId

from auth.auth_bearer import JWTBearer
from utils.redis_helper import check_redis_cache, get_appointment, store_appointment, delete_appointment

from schema.schemas import individual_schema, many_schema

router = APIRouter()
appointment_collection = db.appointments


@router.post("/appointments", dependencies=[Depends(JWTBearer())], tags=["appointments"])
async def create_appointment(appointment: AppointmentModel = Body(...)):
    appointment_data = appointment_collection.insert_one(appointment.dict())

    appointment_id = str(appointment_data.inserted_id)
    store_appointment(appointment_id, appointment)
    return {"message": "Appointment created successfully"}



@router.get("/appointments", dependencies=[Depends(JWTBearer())], tags=["appointments"])
async def get_all_appointments():
    appointments = appointment_collection.appointments.find()
    return many_schema(appointments)


@router.get("/appointments/{appointment_id}", dependencies=[Depends(JWTBearer())], tags=["appointments"])
async def get_appointment(appointment_id: str):
    if check_redis_cache(appointment_id, "appointment"):
        return get_appointment(appointment_id)
    appointment = appointment_collection.appointments.find_one(
        {"_id": ObjectId(appointment_id)}
    )
    if appointment:
        store_appointment(appointment_id, appointment)
        return appointment
    raise HTTPException(status_code=404, detail="Appointment not found")


@router.put("/appointments/{appointment_id}", dependencies=[Depends(JWTBearer())], tags=["appointments"])
async def update_appointment(
    appointment_id: str, appointment: AppointmentModel = Body(...)
):
    updated_appointment = appointment_collection.appointments.find_one_and_update(
        {"_id": ObjectId(appointment_id)},
        {"$set": appointment.dict()},
        return_document=True,
    )
    if updated_appointment:
        store_appointment(appointment_id, updated_appointment)
        return updated_appointment
    raise HTTPException(status_code=404, detail="Appointment not found")


@router.delete("/appointments/{appointment_id}", dependencies=[Depends(JWTBearer())], tags=["appointments"])
async def delete_appointment(appointment_id: str):
    deleted_appointment = appointment_collection.appointments.find_one_and_delete(
        {"_id": ObjectId(appointment_id)}
    )
    if deleted_appointment:
        delete_appointment(appointment_id)
        return {"message": "Appointment deleted successfully"}
    raise HTTPException(status_code=404, detail="Appointment not found")
