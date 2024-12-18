import pandas as pd
import numpy as np
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb+srv://tcr21cs003:1234@cluster0.7yqfh.mongodb.net/?retryWrites=true&w=majority")
db = client["recommedn_db"]

def mean_absolute_error(actual, predicted):
    """Calculate MAE."""
    return np.mean(np.abs(actual - predicted))

def root_mean_square_error(actual, predicted):
    """Calculate RMSE."""
    return np.sqrt(np.mean((actual - predicted) ** 2))

def fetch_data():
    """Fetch actual and predicted data from the database."""
    # Fetch actual ratings from the database
    actual_ratings = pd.DataFrame(list(db["rated_posts"].find()))
    # Ensure required columns exist
    actual_ratings = actual_ratings[["user_id", "post_id", "actual_score"]]

    # Fetch predicted ratings from your recommendation system's predictions collection
    predicted_ratings = pd.DataFrame(list(db["predicted_ratings"].find()))
    # Ensure required columns exist
    predicted_ratings = predicted_ratings[["user_id", "post_id", "predicted_score"]]

    return actual_ratings, predicted_ratings

def evaluate_recommendations():
    """Evaluate recommendations using MAE and RMSE."""
    # Fetch data from the database
    actual_ratings, predicted_ratings = fetch_data()

    # Merge actual and predicted ratings
    evaluation_data = pd.merge(
        actual_ratings,
        predicted_ratings,
        on=["user_id", "post_id"],
        how="inner"  # Ensure only common user-post pairs are evaluated
    )

    # Extract actual and predicted scores
    actual = evaluation_data["actual_score"].values
    predicted = evaluation_data["predicted_score"].values

    # Calculate metrics
    mae = mean_absolute_error(actual, predicted)
    rmse = root_mean_square_error(actual, predicted)

    return mae, rmse

if __name__ == "__main__":
    try:
        mae, rmse = evaluate_recommendations()
        print(f"Mean Absolute Error (MAE): {mae}")
        print(f"Root Mean Square Error (RMSE): {rmse}")
    except Exception as e:
        print(f"Error during evaluation: {e}")
