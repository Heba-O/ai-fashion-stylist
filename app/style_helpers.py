# app/style_helpers.py

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

def recommend_outfit(user_input, data, season=None, occasion=None, color=None):
    # Optional filters
    if season:
        data = data[data['season'].str.lower() == season.lower()]
    if occasion:
        data = data[data['occasion'].str.lower() == occasion.lower()]
    if color:
        data = data[data['color'].str.lower() == color.lower()]

    if data.empty:
        return None

    # Vectorization and similarity matching
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(data["style_notes"].astype(str).tolist() + [user_input])
    cosine_sim = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
    top_index = cosine_sim[0].argsort()[-1]

    return data.iloc[top_index]
