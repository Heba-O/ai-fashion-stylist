# app/style_helpers.py

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

def recommend_outfit(user_input, data, season=None, occasion=None, color=None):
    # Create a copy of the data to apply filters
    filtered = data.copy()

    # Clean up the color column and user input by stripping spaces and lowercasing
    if color:
        color = color.strip().lower()
        filtered = filtered[filtered['color'].str.strip().str.lower() == color]

    # Apply other filters
    if season:
        filtered = filtered[filtered['season'].str.lower() == season.lower()]
    if occasion:
        filtered = filtered[filtered['occasion'].str.lower() == occasion.lower()]

    # If filtered result is empty, fallback to full dataset
    if filtered.empty:
        filtered = data

    # Vectorization and similarity scoring
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(filtered["style_notes"].astype(str).tolist() + [user_input])
    cosine_sim = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
    
    # Get the index of the most similar outfit
    top_index = cosine_sim[0].argsort()[-1]

    return filtered.iloc[top_index]
