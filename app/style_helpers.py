# app/style_helpers.py

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

def recommend_outfit(user_input, data, season=None, occasion=None, color=None, top_n=3):
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
    
    # Start with a copy of the dataset so we don't change the original
    filtered = data.copy()

    # 🧊 Soft filtering - based on season and occasion
    if season:
        filtered = filtered[filtered['season'].str.lower() == season.lower()]
    if occasion:
        filtered = filtered[filtered['occasion'].str.lower() == occasion.lower()]

    # 🧯 If filters result in no matches, fall back to the full dataset
    if filtered.empty:
        filtered = data

    # 🧠 Convert style notes to TF-IDF vectors to measure how similar they are to user input
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(filtered["style_notes"].astype(str).tolist() + [user_input])

    # 🧮 Compute cosine similarity between the user's input and each outfit's style_notes
    cosine_sim = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1]).flatten()

    # 🎯 Get the indices of the top matches (more than top_n so we can filter by color later)
    top_indices = cosine_sim.argsort()[::-1][:top_n * 2]  # More results to allow filtering later

    # 💥 Select the matching outfits
    top_matches = filtered.iloc[top_indices]

    # 🎨 Apply color filter strictly after top-N selection
    if color:
        top_matches_filtered = top_matches[top_matches['color'].str.lower() == color.lower()]
        if not top_matches_filtered.empty:
            top_matches = top_matches_filtered

    # 🚀 Return the top N results as a list of dictionaries
    return top_matches.head(top_n).to_dict(orient="records")
