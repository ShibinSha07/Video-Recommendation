from pymongo import MongoClient
from DB.utils.fetch_all_post import fetch_data

# MongoDB setup
client = MongoClient("mongodb+srv://tcr21cs003:1234@cluster0.7yqfh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.recommedn_db
collection = db["all_posts"]

# API URL and Headers
all_posts_url = "https://api.socialverseapp.com/posts/summary/get?page=1&page_size=1000"
headers = {
    "Flic-Token": "flic_6e2d8d25dc29a4ddd382c2383a903cf4a688d1a117f6eb43b35a1e7fadbb84b8"
}

# Fetch Data
fetch_data(all_posts_url, collection, headers=headers)
