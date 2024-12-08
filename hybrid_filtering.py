from sklearn.preprocessing import MinMaxScaler
from collaborative_filtring import recommend_collaborative
from content_based import content_based_recommendations
import pandas as pd
from pymongo import MongoClient
from sklearn.metrics.pairwise import cosine_similarity

# Connect to MongoDB
client = MongoClient("mongodb+srv://tcr21cs003:1234@cluster0.7yqfh.mongodb.net/?retryWrites=true&w=majority")
db = client["recommedn_db"]

# Load the viewed_posts collection
viewed_posts = list(db["viewed_posts"].find())
post_stats = list(db["post_statistics"].find())
post_stats_df = pd.DataFrame(post_stats)

# Normalize numerical features
scaler = MinMaxScaler()
features = scaler.fit_transform(post_stats_df[['avg_likes', 'share_ratio', 'avg_inspired']])

# Compute content-based similarity

similarity_matrix = cosine_similarity(features)

# Use the similarity matrix in your recommendation system

def recommend_hybrid(user_id, similarity_matrix, top_n=10, weight_content=0.5, weight_collab=0.5):
    """
    Hybrid recommendation combining content-based and collaborative filtering.
    
    Parameters:
        user_id (int): ID of the user for recommendations.
        similarity_matrix (numpy.array): Precomputed similarity matrix for content-based filtering.
        top_n (int): Number of recommendations to return.
        weight_content (float): Weight for content-based recommendations.
        weight_collab (float): Weight for collaborative filtering recommendations.

    Returns:
        List[int]: List of recommended post IDs.
    """
    try:
        # Step 1: Get content-based recommendations
        content_recs = content_based_recommendations(user_id, similarity_matrix, top_n)
        content_scores = {post_id: 1.0 / (rank + 1) for rank, post_id in enumerate(content_recs)}

        # Step 2: Get collaborative recommendations
        try:
            collab_recs = recommend_collaborative(user_id, top_n=top_n)
            collab_scores = {post_id: 1.0 / (rank + 1) for rank, post_id in enumerate(collab_recs)}
        except ValueError:
            print(f"User ID {user_id} not found in interaction matrix. Using only content-based recommendations.")
            collab_scores = {}

        # Step 3: Combine scores from both methods
        combined_scores = {}
        for post_id, score in content_scores.items():
            combined_scores[post_id] = combined_scores.get(post_id, 0) + weight_content * score
        for post_id, score in collab_scores.items():
            combined_scores[post_id] = combined_scores.get(post_id, 0) + weight_collab * score

        # Step 4: Sort and return recommendations
        recommendations = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)[:top_n]

        # Step 5: Fallback to popular posts if no recommendations
        if not recommendations:
            print("No recommendations found. Returning fallback popular posts.")
            popular_posts = (
                pd.DataFrame(viewed_posts)
                .groupby('post_id')
                .size()
                .nlargest(top_n)
                .index
                .tolist()
            )
            return popular_posts

        return [post[0] for post in recommendations]
    except Exception as e:
        print(f"Error in hybrid recommendation: {e}")
        return []

# Example Usage
try:
    # Pass the similarity_matrix precomputed for content-based filtering
    # similarity_matrix = ...  # Placeholder for the actual matrix
    recommended_posts = recommend_hybrid(user_id=53, similarity_matrix=similarity_matrix, top_n=10)
    print(f"Recommended posts for user 23: {recommended_posts}")
except Exception as e:
    print(f"Error during recommendation: {e}")
