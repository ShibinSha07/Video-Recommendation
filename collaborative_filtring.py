from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb+srv://tcr21cs003:1234@cluster0.7yqfh.mongodb.net/?retryWrites=true&w=majority")
db = client["recommedn_db"]

# Load the viewed_posts collection
viewed_posts = list(db["viewed_posts"].find())  # Fetch data as a list
viewed_posts_df = pd.DataFrame(viewed_posts)  # Convert the list to a DataFrame

# Ensure data has the required columns
viewed_posts_df = viewed_posts_df[['user_id', 'post_id', 'viewed_at']]

# Create the user-item interaction matrix
interaction_matrix = viewed_posts_df.pivot_table(
    index='user_id',
    columns='post_id',
    values='viewed_at',
    aggfunc='count',
    fill_value=0
)

# Calculate user-user similarity using cosine similarity
user_similarity = cosine_similarity(interaction_matrix)

# Define the recommendation function
def recommend_collaborative(user_id, top_n=10):
    """Recommend posts using collaborative filtering."""
    # Validate if user exists in the interaction matrix
    if user_id not in interaction_matrix.index:
        raise ValueError(f"User ID {user_id} not found in interaction matrix.")

    # Get user index
    user_idx = interaction_matrix.index.get_loc(user_id)
    
    # Get similarity scores for the user
    similar_users = user_similarity[user_idx]
    
    # Get weighted average of other users' interactions
    scores = interaction_matrix.T.dot(similar_users) / similar_users.sum()
    
    # Exclude posts the user has already interacted with
    user_interactions = interaction_matrix.loc[user_id]
    scores = scores[~user_interactions.astype(bool)]
    
    # Sort and return top_n recommendations
    recommendations = scores.nlargest(top_n).index.tolist()
    return recommendations

# Example usage: Get recommendations for a user
# try:
#     recommended_posts = recommend_collaborative(user_id=50, top_n=10)
#     print(recommended_posts)
# except ValueError as e:
#     print(e)
