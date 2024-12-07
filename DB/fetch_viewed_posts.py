from pymongo import MongoClient
from utils.fetch import fetch_data

# MongoDB setup
client = MongoClient("mongodb+srv://tcr21cs003:1234@cluster0.7yqfh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.recommedn_db
collection = db["viewed_posts"]

# API URL
viewed_posts_url = "https://api.socialverseapp.com/posts/view?page=1&page_size=1000&resonance_algorithm=your_algorithm"

# Fetch Data
fetch_data(viewed_posts_url, collection)
