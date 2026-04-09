import requests

url = "http://127.0.0.1:5000/add-data"

data = {
    "water_level": 75,
    "rain": True
}

response = requests.post(url, json=data)

print(response.json())