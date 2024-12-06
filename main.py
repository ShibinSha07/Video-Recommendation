from fastapi import FastAPI, Query, Header, HTTPException
from typing import Optional, List

app = FastAPI()

# Simulated data storage (for demonstration purposes)
POSTS = [{"id": i, "title": f"Post {i}", "content": f"This is post {i}."} for i in range(1, 1001)]
USERS = [{"id": i, "name": f"User {i}"} for i in range(1, 501)]

# Authorization token for header validation
AUTH_TOKEN = "flic_6e2d8d25dc29a4ddd382c2383a903cf4a688d1a117f6eb43b35a1e7fadbb84b8"

# Helper function to fetch paginated data
def get_paginated_data(data: List[dict], page: int, page_size: int):
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    return data[start_index:end_index]

@app.get("/posts/view")
def get_viewed_posts(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=1000),
    resonance_algorithm: Optional[str] = None,
):
    """
    Get all viewed posts with pagination and optional resonance algorithm.
    """
    paginated_posts = get_paginated_data(POSTS, page, page_size)
    return {
        "page": page,
        "page_size": page_size,
        "resonance_algorithm": resonance_algorithm,
        "total_posts": len(POSTS),
        "posts": paginated_posts,
    }

@app.get("/posts/like")
def get_liked_posts(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=1000),
    resonance_algorithm: Optional[str] = None,
):
    """
    Get all liked posts with pagination and optional resonance algorithm.
    """
    paginated_posts = get_paginated_data(POSTS, page, page_size)
    return {
        "page": page,
        "page_size": page_size,
        "resonance_algorithm": resonance_algorithm,
        "total_posts": len(POSTS),
        "posts": paginated_posts,
    }

@app.get("/posts/inspire")
def get_inspired_posts(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=1000),
    resonance_algorithm: Optional[str] = None,
):
    """
    Get all inspired posts with pagination and optional resonance algorithm.
    """
    paginated_posts = get_paginated_data(POSTS, page, page_size)
    return {
        "page": page,
        "page_size": page_size,
        "resonance_algorithm": resonance_algorithm,
        "total_posts": len(POSTS),
        "posts": paginated_posts,
    }

@app.get("/posts/rating")
def get_rated_posts(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=1000),
    resonance_algorithm: Optional[str] = None,
):
    """
    Get all rated posts with pagination and optional resonance algorithm.
    """
    paginated_posts = get_paginated_data(POSTS, page, page_size)
    return {
        "page": page,
        "page_size": page_size,
        "resonance_algorithm": resonance_algorithm,
        "total_posts": len(POSTS),
        "posts": paginated_posts,
    }

@app.get("/posts/summary/get")
def get_all_posts(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=1000),
    flic_token: str = Header(None),
):
    """
    Get all posts with pagination (authorization required).
    """
    if flic_token != AUTH_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid authorization token")
    
    paginated_posts = get_paginated_data(POSTS, page, page_size)
    return {
        "page": page,
        "page_size": page_size,
        "total_posts": len(POSTS),
        "posts": paginated_posts,
    }

@app.get("/users/get_all")
def get_all_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=1000),
    flic_token: str = Header(None),
):
    """
    Get all users with pagination (authorization required).
    """
    if flic_token != AUTH_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid authorization token")

    paginated_users = get_paginated_data(USERS, page, page_size)
    return {
        "page": page,
        "page_size": page_size,
        "total_users": len(USERS),
        "users": paginated_users,
    }
