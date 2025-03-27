# generates the ezkl proofs that can be verified by the user as well as on the server 
# The server is then sent the training result 

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load datasets
ads_df = pd.read_csv("../trainingdata/ads_content.csv")  # Contains 'adId', 'title', 'description', 'category', 'tags'
interactions_df = pd.read_csv("../trainingdata/user_ad_interactions.csv")  # Contains 'userId', 'adId', 'action'

# Assign scores based on action
interactions_df["score"] = interactions_df["action"].map({"click": 1.0, "view": 0.5})

# Combine relevant text fields for TF-IDF
ads_df["content_combined"] = ads_df["title"] + " " + ads_df["description"] + " " + ads_df["tags"]

# Compute TF-IDF vectors
vectorizer = TfidfVectorizer(stop_words="english")
tfidf_matrix = vectorizer.fit_transform(ads_df["content_combined"])

# Function to compute user profile vector
def get_user_profile(user_id, interactions_df, tfidf_matrix, ads_df):
    user_interactions = interactions_df[interactions_df["userId"] == user_id]

    if user_interactions.empty:
        return None  # No interactions

    # Get interacted ad IDs and their respective scores
    interacted_ads = user_interactions[["adId", "score"]].values

    if len(interacted_ads) == 0:
        return None  # No interactions

    # Compute weighted average TF-IDF vector
    weighted_sum_vector = np.zeros(tfidf_matrix.shape[1])
    total_weight = 0

    for adId, score in interacted_ads:
        ad_index = ads_df.index[ads_df["adId"] == adId].tolist()
        if ad_index:
            weighted_sum_vector += tfidf_matrix[ad_index[0]].toarray()[0] * score
            total_weight += score

    user_profile = weighted_sum_vector / total_weight if total_weight > 0 else weighted_sum_vector
    return user_profile.reshape(1, -1)

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
    top_ads = ads_df.sort_values(by="similarity", ascending=False).head(top_n)[["adId", "similarity"]]

    return top_ads

# Get recommendations for a user
# can get recommendations for any user 
# user_id_to_recommend = "4f3aecdc-f7d8-4718-925c-96d81c3765f3"
# these shall be sent to the server for processing after encryption though. 
def recommendations(user_id_to_recommend):
    recommended_ads = recommend_ads(user_id_to_recommend, interactions_df, tfidf_matrix, ads_df)
    print(recommended_ads)
