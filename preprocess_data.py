from pymongo import MongoClient
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np

# Connect to MongoDB
client = MongoClient("mongodb+srv://tcr21cs003:1234@cluster0.7yqfh.mongodb.net/?retryWrites=true&w=majority")
db = client["recommedn_db"]

# Load collections
viewed_posts = list(db["viewed_posts"].find())
liked_posts = list(db["liked_posts"].find())
inspired_posts = list(db["inspired_posts"].find())
rated_posts = list(db["rated_posts"].find())
all_posts = list(db["all_posts"].find())
users = list(db["users"].find())

# Convert to DataFrames for easy processing
df_viewed = pd.DataFrame(viewed_posts)
df_liked = pd.DataFrame(liked_posts)
df_inspired = pd.DataFrame(inspired_posts)
df_rated = pd.DataFrame(rated_posts)
df_all_posts = pd.DataFrame(all_posts)
df_users = pd.DataFrame(users)


# Identify missing values
print("Missing values in Viewed Posts:", df_viewed.isnull().sum())
print("Missing values in Liked Posts:", df_liked.isnull().sum())
print("Missing values in Inspired Posts:", df_inspired.isnull().sum())
print("Missing values in Rated Posts:", df_rated.isnull().sum())
print("Missing values in All Posts:", df_all_posts.isnull().sum())
print("Missing values in Users:", df_users.isnull().sum())

# Fill missing social media URLs with a placeholder
df_users['instagram-url'].fillna('Not provided', inplace=True)
df_users['youtube_url'].fillna('Not provided', inplace=True)
df_users['tictok_url'].fillna('Not provided', inplace=True)

# Convert DataFrame back to dictionary format for MongoDB
cleaned_users_data = df_users.to_dict('records')

# Update MongoDB collection
db["preprocessed_users"].delete_many({})  # Clear the collection before inserting cleaned data
db["preprocessed_users"].insert_many(cleaned_users_data)

print("Missing values in Users after preprocessing:", df_users.isnull().sum())

# Normalize numeric fields
scaler = MinMaxScaler()

# Users table normalization
numeric_fields_users = ['share_count', 'post_count', 'following_count', 'follower_count']
df_users[numeric_fields_users] = scaler.fit_transform(df_users[numeric_fields_users])

# Rated Posts table normalization
df_rated['rating_percent'] = scaler.fit_transform(df_rated[['rating_percent']])

# Save the preprocessed data back to MongoDB
db["normalized_users"].delete_many({})
db["normalized_users"].insert_many(df_users.to_dict("records"))

db["normalized_rated_posts"].delete_many({})
db["normalized_rated_posts"].insert_many(df_rated.to_dict("records"))

print("Data preprocessing and normalization completed successfully.")

# Feature Engineering

# Derive interaction frequencies for users
user_interactions = pd.DataFrame()

# Group interactions by user_id
user_interactions['total_views'] = df_viewed.groupby('user_id')['post_id'].count()
user_interactions['total_likes'] = df_liked.groupby('user_id')['post_id'].count()
user_interactions['total_inspired'] = df_inspired.groupby('user_id')['post_id'].count()

# Fill missing values with 0 for users without specific interactions
user_interactions.fillna(0, inplace=True)

# Normalize user interaction features
user_interactions[['total_views', 'total_likes', 'total_inspired']] = scaler.fit_transform(
    user_interactions[['total_views', 'total_likes', 'total_inspired']]
)

# Save user interaction frequencies back to MongoDB
user_interactions.reset_index(inplace=True)
db["user_interactions"].delete_many({})
db["user_interactions"].insert_many(user_interactions.to_dict("records"))

# Aggregate statistics for posts
post_stats = pd.DataFrame()

# Fix division by zero in view_count
df_all_posts['view_count'] = df_all_posts['view_count'].replace(0, 1)

# Calculate post statistics
post_stats['avg_likes'] = df_liked.groupby('post_id')['user_id'].count() / df_all_posts['view_count']
post_stats['avg_inspired'] = df_inspired.groupby('post_id')['user_id'].count() / df_all_posts['view_count']
post_stats['share_ratio'] = df_all_posts['share_count'] / df_all_posts['view_count']

# Replace inf and NaN values with 0
post_stats.replace([np.inf, -np.inf], 0, inplace=True)
post_stats.fillna(0, inplace=True)

# Normalize post stats
post_stats[['avg_likes', 'avg_inspired', 'share_ratio']] = scaler.fit_transform(
    post_stats[['avg_likes', 'avg_inspired', 'share_ratio']]
)



# # Group interactions by post_id
# post_stats['avg_likes'] = df_liked.groupby('post_id')['user_id'].count() / df_all_posts['view_count']
# post_stats['avg_inspired'] = df_inspired.groupby('post_id')['user_id'].count() / df_all_posts['view_count']
# post_stats['share_ratio'] = df_all_posts['share_count'] / df_all_posts['view_count']

# # print(post_stats[['avg_likes', 'avg_inspired', 'share_ratio']].describe())
# # print(post_stats[['avg_likes', 'avg_inspired', 'share_ratio']].isna().sum())
# # print(post_stats[['avg_likes', 'avg_inspired', 'share_ratio']].head())

# df_all_posts['view_count'] = df_all_posts['view_count'].replace(0, 1)
# post_stats.replace([np.inf, -np.inf], 0, inplace=True)
# post_stats.fillna(0, inplace=True)

# # # Fill missing values with 0 for posts with no interactions
# post_stats.fillna(0, inplace=True)

# # # Normalize post stats
# # post_stats[['avg_likes', 'avg_inspired', 'share_ratio']] = scaler.fit_transform(
# #     post_stats[['avg_likes', 'avg_inspired', 'share_ratio']]
# # )

# Save post stats back to MongoDB
post_stats.reset_index(inplace=True)
db["post_statistics"].delete_many({})
db["post_statistics"].insert_many(post_stats.to_dict("records"))

# Check the min and max values of the features after normalization
print(post_stats[['avg_likes', 'avg_inspired', 'share_ratio']].min())
print(post_stats[['avg_likes', 'avg_inspired', 'share_ratio']].max())

# Check a random sample of rows
print(post_stats.sample(10))


print("Feature engineering completed successfully.")
