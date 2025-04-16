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

    # Apply filters if selected
    if season:
        filtered = filtered[filtered['season'].str.lower() == season.lower()]
    if occasion:
        filtered = filtered[filtered['occasion'].str.lower() == occasion.lower()]
    if color:
        filtered = filtered[filtered['color'].str.lower() == color.lower()]

    # Fallback to full dataset if no matches
    if filtered.empty:
        filtered = data

    # Create TF-IDF matrix using style notes and user input
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(filtered["style_notes"].astype(str).tolist() + [user_input])

    # Calculate cosine similarity between user input and outfit notes
    cosine_sim = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1]).flatten()

    # Get indices of top N matches
    top_indices = cosine_sim.argsort()[::-1][:top_n]

    # Return top matches as a list of dictionaries
    return filtered.iloc[top_indices].to_dict(orient="records")
