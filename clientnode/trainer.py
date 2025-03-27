# generates the ezkl proofs that can be verified by the user as well as on the server 
# The server is then sent the training result 
import ezkl
import torch
import torch.nn as nn
import torch.onnx
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
tfidf_tensor = torch.tensor(tfidf_matrix.toarray(), dtype=torch.float32)

# PyTorch Model for Recommendation
class RecommendationModel(nn.Module):
    def __init__(self, tfidf_matrix):
        super(RecommendationModel, self).__init__()
        self.tfidf_matrix = nn.Parameter(torch.tensor(tfidf_matrix.toarray(), dtype=torch.float32), requires_grad=False)

    def forward(self, user_profile):
        similarity = torch.nn.functional.cosine_similarity(user_profile, self.tfidf_matrix, dim=1)
        return similarity

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
    return torch.tensor(user_profile.reshape(1, -1), dtype=torch.float32)

# Export the model to ONNX format
user_profile_dummy = torch.rand(1, tfidf_matrix.shape[1])  # Dummy user profile for export

model = RecommendationModel(tfidf_matrix)
onnx_path = "network.onnx"

torch.onnx.export(model, user_profile_dummy, onnx_path, opset_version=10)

print(f"Model exported to {onnx_path}")
