# app/style_helpers.py

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

def recommend_outfits(user_input, data, season=None, occasion=None, color=None, top_n=3):
    """
    Recommend top N outfits based on user input description and optional filters.

    Parameters:
        user_input (str): Free-text style description from the user.
        data (pd.DataFrame): Outfit dataset containing style_notes, color, season, etc.
        season (str): Optional season filter (e.g., 'Autumn').
        occasion (str): Optional occasion filter (e.g., 'Date').
        color (str): Optional color filter (e.g., 'Red').
        top_n (int): Number of outfit suggestions to return (default is 3).

    Returns:
        List[Dict]: A list of outfit dictionaries matching user input and filters.
    """
    filtered = data.copy()

    # Apply soft filters
    if season:
        filtered = filtered[filtered['season'].str.lower() == season.lower()]
    if occasion:
        filtered = filtered[filtered['occasion'].str.lower() == occasion.lower()]

    # Fallback to full dataset if too filtered
    if filtered.empty:
        filtered = data

    # Vectorization
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(filtered["style_notes"].astype(str).tolist() + [user_input])

    # Similarity scoring
    cosine_sim = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1]).flatten()
    top_indices = cosine_sim.argsort()[::-1][:top_n * 2]  # Get more than needed to filter later

    top_matches = filtered.iloc[top_indices]

    # Enforce color preference after top-N similarity
    if color:
        top_matches_filtered = top_matches[top_matches['color'].str.lower() == color.lower()]
        if not top_matches_filtered.empty:
            top_matches = top_matches_filtered

    # Limit to top N results
    return top_matches.head(top_n).to_dict(orient="records")
