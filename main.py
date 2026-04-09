from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

from sms_service import send_sms

app = FastAPI()

latest_data = {
    "water_level": 0,
    "rain": 0,
    "temperature": 0,
    "humidity": 0,
    "risk": "LOW",
    "alert": False,
    "last_update": None
}

class SensorData(BaseModel):
    water_level: int
    rain: int
    temperature: int
    humidity: int

def calculate_risk(water_level, rain, humidity):
    score = water_level

    if rain > 0:
        score += 20
    if humidity > 80:
        score += 10

    prev = latest_data.get("risk", "LOW")

    if prev == "HIGH":
        return "HIGH" if score >= 75 else "MEDIUM"
    elif prev == "MEDIUM":
        if score >= 90:
            return "HIGH"
        elif score < 45:
            return "LOW"
        else:
            return "MEDIUM"
    else:
        return "MEDIUM" if score >= 60 else "LOW"

@app.post("/update")
def update_data(data: SensorData):
    global latest_data

    risk = calculate_risk(data.water_level, data.rain, data.humidity)

    alert = True if risk == "HIGH" else False

    latest_data = {
        "water_level": data.water_level,
        "rain": data.rain,
        "temperature": data.temperature,
        "humidity": data.humidity,
        "risk": risk,
        "alert": alert,
        "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    print("DATA RECEIVED:", latest_data)

    if alert:
        print("ALERT TRIGGERED")
        send_sms(data.water_level)

    return {"status": "updated", "data": latest_data}

@app.get("/latest")
def get_latest():
    return latest_data