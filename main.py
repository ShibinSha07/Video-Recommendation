# import requests

# BASE_URL = "https://api.socialverseapp.com"
# HEADERS = {
#     "Flic-Token": "flic_6e2d8d25dc29a4ddd382c2383a903cf4a688d1a117f6eb43b35a1e7fadbb84b8"
# }

# def fetch_data(endpoint, params):
#     response = requests.get(f"{BASE_URL}{endpoint}", headers=HEADERS, params=params)
#     if response.status_code == 200:
#         return response.json()
#     else:
#         print(f"Error fetching data: {response.status_code}")
#         return []

# def fetch_paginated_data(endpoint):
#     page = 1
#     page_size = 1000
#     all_data = []
    
#     while True:
#         params = {"page": page, "page_size": page_size}
#         data = fetch_data(endpoint, params)
#         if not data or len(data) < page_size:
#             break
#         all_data.extend(data)
#         page += 1
    
#     return all_data

# # Example usage
# viewed_posts = fetch_paginated_data("/posts/view")
# liked_posts = fetch_paginated_data("/posts/like")
