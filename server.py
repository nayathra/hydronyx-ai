from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime
import numpy as np
from sklearn.linear_model import LinearRegression

app = Flask(__name__)

# MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["hydronyx_db"]
collection = db["sensor_data"]

# ─────────────────────────────────────────────
# Risk Logic (improved)
def calculate_risk(water, rain):
    score = water + (20 if rain else 0)

    if score >= 90:
        return "HIGH"
    elif score >= 55:
        return "MEDIUM"
    return "LOW"


# ─────────────────────────────────────────────
# API 1: Ingest Data (from ESP32 or UI)
@app.route('/ingest', methods=['POST'])
def ingest():
    data = request.json

    water = data.get("water_level")
    rain = data.get("rain")

    if water is None:
        return jsonify({"error": "Missing water_level"}), 400

    risk = calculate_risk(water, rain)

    record = {
        "water_level": water,
        "rain": rain,
        "risk": risk,
        "timestamp": datetime.utcnow()
    }

    collection.insert_one(record)

    return jsonify({
        "message": "Stored successfully",
        "risk": risk
    })


# ─────────────────────────────────────────────
# API 2: Get Latest Data
@app.route('/latest', methods=['GET'])
def latest():
    data = collection.find_one(sort=[("_id", -1)])

    if not data:
        return jsonify({"error": "No data"}), 404

    return jsonify({
        "water_level": data["water_level"],
        "rain": data["rain"],
        "risk": data["risk"],
        "timestamp": data["timestamp"]
    })


# ─────────────────────────────────────────────
# API 3: History (last N readings)
@app.route('/history', methods=['GET'])
def history():
    records = list(collection.find().sort("_id", -1).limit(20))

    output = []
    for r in records:
        output.append({
            "water_level": r["water_level"],
            "rain": r["rain"],
            "risk": r["risk"],
            "timestamp": r["timestamp"]
        })

    return jsonify(output)


# ─────────────────────────────────────────────
# AI Prediction (Linear Regression)
@app.route('/predict', methods=['GET'])
def predict():
    data = list(collection.find().sort("_id", 1))

    if len(data) < 5:
        return jsonify({"error": "Not enough data"}), 400

    # Prepare dataset
    X = []
    y = []

    for i, d in enumerate(data):
        X.append([i])  # time index
        y.append(d["water_level"])

    X = np.array(X)
    y = np.array(y)

    model = LinearRegression()
    model.fit(X, y)

    # Predict next 5 steps
    future = np.array([[len(X) + i] for i in range(5)])
    predictions = model.predict(future)

    return jsonify({
        "future_levels": predictions.tolist(),
        "trend": "RISING" if predictions[-1] > y[-1] else "FALLING"
    })


# ─────────────────────────────────────────────
# Alert System
@app.route('/alert', methods=['GET'])
def alert():
    data = collection.find_one(sort=[("_id", -1)])

    if data["risk"] == "HIGH":
        return jsonify({
            "alert": True,
            "message": "🚨 Flood Risk High! Evacuate!"
        })

    return jsonify({
        "alert": False,
        "message": "Safe"
    })


# ─────────────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=True)