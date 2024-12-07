import requests

def fetch_data(api_url, collection, headers=None):
    page = 1
    while True:
        url = api_url.replace("page=1", f"page={page}")
        response = requests.get(url, headers=headers)
        data = response.json()

        if not data.get("posts"):  # Stop if no posts are returned
            break

        for item in data["posts"]:
            # Deduplicate using post_id
            if collection.count_documents({"post_id": item["post_id"]}) == 0:
                collection.insert_one(item)
        print(f"Fetched page {page} for {collection.name}")
        page += 1
