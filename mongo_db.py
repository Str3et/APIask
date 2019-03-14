from pymongo import MongoClient


client = MongoClient()
database = client.database
data_db = database.email
