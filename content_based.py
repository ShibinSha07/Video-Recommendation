from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb+srv://tcr21cs003:1234@cluster0.7yqfh.mongodb.net/?retryWrites=true&w=majority")
db = client["recommedn_db"]

# Load collections
post_stats = list(db["post_statistics"].find())  # Returns a list
post_stats_df = pd.DataFrame(post_stats)  # Convert the list to a DataFrame

# Ensure the required columns are numeric and handle missing values
post_stats_df[['avg_likes', 'avg_inspired', 'share_ratio']] = post_stats_df[['avg_likes', 'avg_inspired', 'share_ratio']].fillna(0).astype(float)

# Extract feature matrix
post_features = post_stats_df[['avg_likes', 'avg_inspired', 'share_ratio']].values

# Compute cosine similarity
similarity_matrix = cosine_similarity(post_features)

# To recommend top N similar posts for a given post:
# def content_based_recommendations(post_idx, similarity_matrix, top_n=10):
#     """Recommend top N similar posts for a given post index."""
#     similar_scores = list(enumerate(similarity_matrix[post_idx]))
#     similar_scores = sorted(similar_scores, key=lambda x: x[1], reverse=True)
#     top_posts = [score[0] for score in similar_scores[1:top_n+1]]  # Skip the first as it's the post itself
#     return top_posts

def content_based_recommendations(post_idx, similarity_matrix, top_n=10):
    """Recommend top N similar posts for a given post index."""
    # Convert post_stats to DataFrame (if not already)
    if not isinstance(post_stats, pd.DataFrame):
        post_stats_df = pd.DataFrame(post_stats)

    # Ensure the DataFrame contains required columns
    if not set(['avg_likes', 'avg_inspired', 'share_ratio']).issubset(post_stats_df.columns):
        raise ValueError("Required columns missing in post statistics data.")

    # Ensure numeric conversion for cosine similarity
    post_stats_df[['avg_likes', 'avg_inspired', 'share_ratio']] = (
        post_stats_df[['avg_likes', 'avg_inspired', 'share_ratio']].fillna(0).astype(float)
    )

    # Extract feature matrix
    post_features = post_stats_df[['avg_likes', 'avg_inspired', 'share_ratio']].values

    # Compute cosine similarity
    similarity_matrix = cosine_similarity(post_features)

    # Get top recommendations
    similar_scores = list(enumerate(similarity_matrix[post_idx]))
    similar_scores = sorted(similar_scores, key=lambda x: x[1], reverse=True)
    top_posts = [score[0] for score in similar_scores[1:top_n+1]]  # Skip the first as it's the post itself
    return top_posts

# Example: Get top 10 recommendations for a post with index 0
# top_recommended_posts = content_based_recommendations(17, similarity_matrix, top_n=10)
# print(top_recommended_posts)

