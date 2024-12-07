from pymongo import MongoClient
from utils.fetch import fetch_data

# MongoDB setup
client = MongoClient("mongodb+srv://tcr21cs003:1234@cluster0.7yqfh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.recommedn_db
collection = db["rated_posts"]

# API URL
rated_posts_url = "https://api.socialverseapp.com/posts/rating?page=1&page_size=1000&resonance_algorithm=resonance_algorithm_cjsvervb7dbhss8bdrj89s44jfjdbsjd0xnjkbvuire8zcjwerui3njfbvsujc5if"
# Fetch Data
fetch_data(rated_posts_url, collection)