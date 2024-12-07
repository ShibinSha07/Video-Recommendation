import requests
from pymongo import MongoClient

# MongoDB connection details
client = MongoClient("mongodb+srv://tcr21cs003:1234@cluster0.7yqfh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.recommedn_db
collection = db["users"]

# API URL and headers
users_url = "https://api.socialverseapp.com/users/get_all?page=1&page_size=1000"
headers = {
    "Flic-Token": "flic_6e2d8d25dc29a4ddd382c2383a903cf4a688d1a117f6eb43b35a1e7fadbb84b8"
}

# Fetch data from API
response = requests.get(users_url, headers=headers)
data = response.json()

# Print the structure of the response
print(f"API Response: {data}")

# Process the data
users = data.get("users", [])
print(f"Users found: {len(users)}")

if users:
    for item in users:
        # Ensure that 'id' is the correct field for unique identification
        unique_id_field = "id"
        print(f"Processing user: {item}")  # Debug: Print user data

        # Check if the user is already in the collection (based on unique 'id')
        if collection.count_documents({unique_id_field: item[unique_id_field]}) == 0:
            collection.insert_one(item)
            print(f"Inserted user with ID: {item[unique_id_field]}")
        else:
            print(f"User with ID {item[unique_id_field]} already exists.")
