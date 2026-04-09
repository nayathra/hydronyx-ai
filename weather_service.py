import requests

API_KEY = "54de85cf56c9f7315c64f02a2dc047c9"

def get_weather(lat, lon):
    try:
        url = "https://api.openweathermap.org/data/2.5/weather"

        params = {
            "lat": lat,
            "lon": lon,
            "appid": API_KEY,
            "units": "metric"
        }

        response = requests.get(url, params=params, timeout=5)

        if response.status_code != 200:
            print("OpenWeather API Error:", response.text)
            return None

        data = response.json()

        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]

        rain = 0
        if "rain" in data and "1h" in data["rain"]:
            rain = data["rain"]["1h"]

        return {
            "temperature": temperature,
            "humidity": humidity,
            "rain": rain
        }

    except requests.exceptions.Timeout:
        print("Weather API Timeout")
        return None

    except Exception as e:
        print("Weather Fetch Error:", e)
        return None