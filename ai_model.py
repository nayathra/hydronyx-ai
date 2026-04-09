import numpy as np

def predict_risk(data):

    if len(data) < 3:
        return {"risk": "LOW"}

    levels = [d["water_level"] for d in data]
    rain = [1 if d.get("rain", 0) > 0 else 0 for d in data]
    humidity = [d.get("humidity", 50) for d in data]

    trend = np.polyfit(range(len(levels)), levels, 1)[0]

    score = (
        levels[-1] * 0.5 +
        rain[-1] * 20 +
        humidity[-1] * 0.2 +
        trend * 10
    )

    if score > 80:
        risk = "HIGH"
    elif score > 50:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    # ⏱ Time to flood
    if trend > 0:
        time_to_flood = round((100 - levels[-1]) / trend)
    else:
        time_to_flood = -1

    return {
        "risk": risk,
        "trend": "Rising" if trend > 0 else "Falling",
        "time_to_flood": f"{time_to_flood} min" if time_to_flood > 0 else "No immediate risk",
        "confidence": round(min(abs(trend)/5, 1), 2)
    }