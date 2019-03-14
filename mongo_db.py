from pymongo import MongoClient


client = MongoClient()
database = client.database
email_db = database.email
account_db = database.account
