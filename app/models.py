from pymongo import MongoClient

client = MongoClient('localhost', 27017)

db = client.github_tracking_tool

accounts_data = db.accounts_data
repositories_data = db.repositories_data