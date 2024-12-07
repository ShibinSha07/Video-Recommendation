# this fetch is for fetch_all_posts.py

import requests
def fetch_data(api_url, collection, headers=None):
    page = 1
    while True:
        url = api_url.replace("page=1", f"page={page}")
        response = requests.get(url, headers=headers)
        data = response.json()

        # Debug: Print the structure of the response
        print(f"API Response (Page {page}): {data}")

        # Ensure the response contains the 'posts' or expected data key
        posts = data.get("posts", [])  # Use the correct key from the response
        if not posts:
            print("No more posts found.")
            break

        for item in posts:
            # Use a valid unique identifier, e.g., 'id' instead of 'post_id' if applicable
            unique_id_field = "id"  # Update this field based on the response structure
            if collection.count_documents({unique_id_field: item[unique_id_field]}) == 0:
                collection.insert_one(item)

        print(f"Fetched page {page} for {collection.name}")
        page += 1
