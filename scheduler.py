import time
import random
from datetime import datetime
from database import collection
from weather_service import get_weather

LAT = 13.0827
LON = 80.2707

def simulate_realtime():
    while True:
        weather = get_weather(LAT, LON)

        if weather:
            data = {
                "water_level": random.randint(30, 100),
                "temperature": weather["temperature"],
                "humidity": weather["humidity"],
                "rain": weather["rain"],
                "lat": LAT,
                "lon": LON,
                "timestamp": datetime.utcnow()
            }

            collection.insert_one(data)
            print("Inserted:", data)

        else:
            print("Weather fetch failed")

        time.sleep(5)