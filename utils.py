def calculate_risk(water, rain):
    score = water + (20 if rain else 0)

    if score >= 90:
        return "HIGH"
    elif score >= 60:
        return "MEDIUM"
    return "LOW"


def get_action(risk):
    if risk == "HIGH":
        return "🚨 Immediate evacuation required"
    elif risk == "MEDIUM":
        return "⚠ Stay alert and monitor"
    return "✅ Safe"