from pymongo import MongoClient

client = MongoClient("mongodb+srv://tcr21cs003:1234@cluster0.7yqfh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.recommedn_db

viewed_posts_collection = db["viewed_posts"]
all_posts_collection = db["all_posts"]
liked_posts_collection = db["liked_posts"]
inspired_posts_collection = db["inspired_posts"]
rated_posts_collection = db["rated_posts"]
user_collection = db["users"]

print(f"Total documents in viewed collection: {viewed_posts_collection.count_documents({})}")
print(f"Total documents in all posts collection: {all_posts_collection.count_documents({})}")
print(f"Total documents in liked collection: {liked_posts_collection.count_documents({})}")
print(f"Total documents in inspired collection: {inspired_posts_collection.count_documents({})}")
print(f"Total documents in rated collection: {rated_posts_collection.count_documents({})}")
print(f"Total documents in user collection: {user_collection.count_documents({})}")

