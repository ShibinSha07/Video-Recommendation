from enum import Enum

from fastapi import FastAPI
from pydantic import BaseModel

app=FastAPI()

class Category(Enum):
    TOOLS="tools"
    CONSUMABLES="consumables"
    
class Item(BaseModel):
    name:str
    price:float
    count:int
    id:int
    category:Category
    
items={
    0:Item(name="A",price=9.99,count=20,id=0,category=Category.TOOLS),
    1:Item(name="B",price=5.99,count=2,id=1,category=Category.TOOLS),
    2:Item(name="C",price=3.99,count=200,id=2,category=Category.CONSUMABLES)
}


@app.get("/")
def index()->dict[str,dict[int,Item]]:
    return {"items":items}

# @app.get("/items/{item_id}")
# def query_item_by_id(item_id:int)->Item:
#     if item_id not in Item:
#         raise HTTPException(
#             status_code=404,details=f"Item with{item_id=} does not exist"
#         )
#     return items[item_id]












# from fastapi import FastAPI
# import requests

# app = FastAPI()

# @app.get("/")
# def read_root():
#     return {"message": "Welcome to the Video Recommendation API!"}

# @app.get("/feed")
# def get_recommendations(username: str, category_id: str = None, mood: str = None):
#     return {
#         "username": username,
#         "category_id": category_id,
#         "mood": mood,
#         "recommendations": ["Video1", "Video2", "Video3"]
#     }

# @app.get("/fetch_data")
# def fetch_data():
#     url = "https://api.socialverseapp.com/posts/view?page=1&page_size=1000"
#     headers = {"Flic-Token": "flic_6e2d8d25dc29a4ddd382c2383a903cf4a688d1a117f6eb43b35a1e7fadbb84b8"}
#     response = requests.get(url, headers=headers)
#     return response.json()
