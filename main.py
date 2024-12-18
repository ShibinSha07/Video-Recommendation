from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from typing import Optional

app = FastAPI()

# Connect to MongoDB
client = MongoClient("mongodb+srv://tcr21cs003:1234@cluster0.7yqfh.mongodb.net/?retryWrites=true&w=majority")
db = client["recommedn_db"]

class RecommendationRequest(BaseModel):
    username: str
    category_id: Optional[int] = None
    mood: Optional[str] = None

def get_recommended_posts(username: str, category_id: Optional[int] = None, mood: Optional[str] = None, top_n: int = 10):
    """
    Generate recommendations based on username, category, and mood.

    Args:
        username (str): Username of the user.
        category_id (int, optional): ID of the category user wants to see.
        mood (str, optional): Current mood of the user.
        top_n (int): Number of recommendations to return.

    Returns:
        list: List of recommended posts.
    """
    # Fetch user details
    user = db["users"].find_one({"username": username})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Fetch recommendations based on filters
    query = {}
    if category_id:
        query["category_id"] = category_id
    if mood:
        query["mood"] = mood

    # Generate recommendations (dummy logic for now)
    recommendations = list(db["posts"].find(query).limit(top_n))

    # Return only necessary fields
    recommended_posts = [
        {"post_id": post["_id"], "title": post["title"], "category_id": post["category_id"], "mood": post.get("mood")}
        for post in recommendations
    ]
    return recommended_posts

@app.get("/feed")
async def feed(request: RecommendationRequest):
    recommended_posts = get_recommended_posts(request.username, request.category_id, request.mood)
    return recommended_posts

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=5000)
