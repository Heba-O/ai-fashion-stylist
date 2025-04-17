# app/style_helpers.py

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fuzzywuzzy import fuzz
import pandas as pd

def color_match(row_color, user_color):
    return fuzz.partial_ratio(row_color.lower(), user_color.lower()) > 80

def recommend_outfit(user_input, data, season=None, occasion=None, color=None, top_n=3):
    """
    Recommend top N outfits based on user input and optional filters.

    Parameters:
        user_input (str): Free-text description (optional).
        data (pd.DataFrame): Dataset of outfits.
        season (str): Season filter.
        occasion (str): Occasion filter.
        color (str): Color filter.
        top_n (int): Number of results to return.

    Returns:
        List[Dict]: List of recommended outfits.
    """
    filtered = data.copy()

    # Soft filtering
    if season:
        filtered = filtered[filtered['season'].str.lower() == season.lower()]
    if occasion:
        filtered = filtered[filtered['occasion'].str.lower() == occasion.lower()]
    if filtered.empty:
        filtered = data

    # Similarity-based ranking (if description is provided)
    if user_input.strip():
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(filtered["style_notes"].astype(str).tolist() + [user_input])
        cosine_sim = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1]).flatten()
        top_indices = cosine_sim.argsort()[::-1][:top_n * 2]
        top_matches = filtered.iloc[top_indices]
    else:
        top_matches = filtered

    # Apply fuzzy color match
    if color:
        top_matches_filtered = top_matches[top_matches['color'].apply(lambda c: color_match(c, color))]
        if not top_matches_filtered.empty:
            top_matches = top_matches_filtered

    return top_matches.head(top_n).to_dict(orient="records")
