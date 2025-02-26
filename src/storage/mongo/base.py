from config import MONGO_DB_NAME, MONGO_URL
from pymongo import MongoClient

client = MongoClient(MONGO_URL)
db = client[MONGO_DB_NAME]