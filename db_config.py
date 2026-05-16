from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["stockdb"]
stocks_collection = db["stocks"]