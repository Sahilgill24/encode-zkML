# generates the ezkl proofs that can be verified by the user as well as on the server 
# The server is then sent the training result 

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load datasets
ads_df = pd.read_csv("../trainingdata/ads_content.csv")  # Contains 'adid', 'title', 'description', 'category', 'tags'
interactions_df = pd.read_csv("../trainingdata/user_ad_interactions.csv")  # Contains 'userId', 'adid', 'score'

# Combine relevant text fields for TF-IDF
ads_df["content_combined"] = ads_df["title"] + " " + ads_df["description"] + " " + ads_df["tags"]

# Compute TF-IDF vectors
vectorizer = TfidfVectorizer(stop_words="english")
tfidf_matrix = vectorizer.fit_transform(ads_df["content_combined"])

# Function to compute user profile vector
def get_user_profile(user_id, interactions_df, tfidf_matrix, ads_df):
    user_interactions = interactions_df[interactions_df["userId"] == user_id]
    interacted_ads = user_interactions[user_interactions["score"] > 0]["adid"].values

    if len(interacted_ads) == 0:
        return None  # No interactions

    ad_indices = ads_df[ads_df["adid"].isin(interacted_ads)].index
    user_tfidf = tfidf_matrix[ad_indices]

    avg_vector = user_tfidf.mean(axis=0)  # Compute average vector
    return avg_vector

# Function to generate recommendations
def recommend_ads(user_id, interactions_df, tfidf_matrix, ads_df, top_n=10):
    user_profile = get_user_profile(user_id, interactions_df, tfidf_matrix, ads_df)
    if user_profile is None:
        return None

    # Compute similarity between user profile and all ads
    similarity_scores = cosine_similarity(user_profile, tfidf_matrix).flatten()

    # Normalize scores
    min_score, max_score = similarity_scores.min(), similarity_scores.max()
    normalized_scores = (similarity_scores - min_score) / (max_score - min_score) if max_score != min_score else 0.5

    # Get top N recommended ads
    ads_df["similarity"] = normalized_scores
    top_ads = ads_df.sort_values(by="similarity", ascending=False).head(top_n)[["adid", "similarity"]]
    
    return top_ads

# Get recommendations for a user
user_id_to_recommend = "4f3aecdc-f7d8-4718-925c-96d81c3765f3"
recommended_ads = recommend_ads(user_id_to_recommend, interactions_df, tfidf_matrix, ads_df)
print(recommended_ads)
