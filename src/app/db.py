import os

from pymongo import MongoClient

client = MongoClient(os.environ["MONGODB_URL"])
db = client.university
annual_university = db.annual_univeristy
latest_university = db.latest_university
top_university = db.top_university
