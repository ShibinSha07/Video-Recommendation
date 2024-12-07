import requests
# from dotenv import load_dotenv
import os
from config.database import db

# Load environment variables
# load_dotenv()
FLIC_TOKEN = os.getenv("FLIC_TOKEN")

# Function to fetch data and insert into MongoDB
def fetch_data(api_url, collection_name):
    headers = {"Flic-Token": FLIC_TOKEN}
    page = 1
    while True:
        url = f"{api_url}&page={page}&page_size=1000"
        response = requests.get(url, headers=headers)

        if response.status_code == 404:
            print(f"Error 404: Not Found. Check the URL or endpoint. URL: {url}")
            break
        elif response.status_code != 200:
            print(f"Error: {response.status_code} - {response.text}")
            break
        
        try:
            data = response.json()  # Parse JSON response
            print(f"API Response (Raw Data): {data}")
        except ValueError as e:
            print(f"Error parsing response: {e}")
            break

        # Ensure data is a dictionary and extract the `posts` key
        if isinstance(data, dict) and "posts" in data:
            posts = data["posts"]
        else:
            print("No 'posts' key found in the response. Stopping.")
            break

        # Check if `posts` is a valid list
        if not isinstance(posts, list) or len(posts) == 0:
            print("No more posts available or invalid format.")
            break

        collection = db[collection_name]
        for item in posts:
            print(f"Current Item: {item}")  # Inspect each item
            if isinstance(item, dict) and "post_id" in item:
                if collection.count_documents({"post_id": item["post_id"]}) == 0:
                    collection.insert_one(item)
                    print(f"Inserted post {item['post_id']}")
                else:
                    print(f"Post {item['post_id']} already exists.")
            else:
                print(f"Skipping invalid item: {item}")

        print(f"Fetched page {page} for {collection_name}")
        page += 1

# API URL
viewed_posts_url = "https://api.socialverseapp.com/posts/view?page=1&page_size=1000&resonance_algorithm=resonance_algorithm_cjsvervb7dbhss8bdrj89s44jfjdbsjd0xnjkbvuire8zcjwerui3njfbvsujc5if"
fetch_data(viewed_posts_url, "viewed_posts")
