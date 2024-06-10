from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.objectid import ObjectId

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["your_database"]  # Replace 'your_database' with your actual database name
appointment_collection = db["appointments"]

# Initialize Flask app
app = Flask(__name__)


# Create a new appointment
@app.route("/appointments", methods=["POST"])
def create_appointment():
    new_appointment = request.json
    appointment_collection.insert_one(new_appointment)
    return jsonify(new_appointment), 201


# Get all appointments
@app.route("/appointments", methods=["GET"])
def get_all_appointments():
    appointments = list(appointment_collection.find())
    return jsonify(appointments), 200


# Get an appointment by ID
@app.route("/appointments/<string:appointment_id>", methods=["GET"])
def get_appointment_by_id(appointment_id):
    appointment = appointment_collection.find_one({"_id": ObjectId(appointment_id)})
    if appointment:
        return jsonify(appointment), 200
    else:
        return jsonify({"error": "Appointment not found"}), 404


# Update an appointment
@app.route("/appointments/<string:appointment_id>", methods=["PUT"])
def update_appointment(appointment_id):
    updated_appointment = request.json
    appointment_collection.update_one(
        {"_id": ObjectId(appointment_id)}, {"$set": updated_appointment}
    )
    return jsonify(updated_appointment), 200


# Delete an appointment
@app.route("/appointments/<string:appointment_id>", methods=["DELETE"])
def delete_appointment(appointment_id):
    appointment_collection.delete_one({"_id": ObjectId(appointment_id)})
    return jsonify({"message": "Appointment deleted successfully"}), 200


# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
