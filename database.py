from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["hydronyx"]
collection = db["sensor_data"]