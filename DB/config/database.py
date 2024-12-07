from pymongo import MongoClient

# MongoDB connection URI
uri = "mongodb+srv://tcr21cs003:1234@cluster0.7yqfh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)
db = client.recommedn_db  # Database name

# This will be used for inserting/retrieving data in other files
