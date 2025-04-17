from sentence_transformers import SentenceTransformer, util
from fuzzywuzzy import fuzz, process
import pandas as pd

# Load model once
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

def color_match(row_color, user_color):
    return fuzz.partial_ratio(row_color.lower(), user_color.lower()) > 80

def filter_by_fuzzy_match(filtered, column, value):
    """ Fuzzy match function for season and occasion. """
    if not value:
        return filtered  # If no value is provided, don't filter
    
    choices = filtered[column].unique()
    best_match, score = process.extractOne(value.lower(), choices)
    if score > 70:  # Threshold for fuzzy match quality
        filtered = filtered[filtered[column].str.lower() == best_match]
    return filtered

def recommend_outfit(user_input, data, season=None, occasion=None, color=None, top_n=3):
    """
    Recommend top N outfits using SentenceTransformer embeddings and optional filters.
    """
    filtered = data.copy()

    # Apply fuzzy matching for season and occasion
    if season:
        filtered = filter_by_fuzzy_match(filtered, 'season', season)
    if occasion:
        filtered = filter_by_fuzzy_match(filtered, 'occasion', occasion)
    
    if filtered.empty:
        filtered = data  # fallback to full dataset

    # Similarity-based ranking
    if user_input.strip():
        descriptions = filtered['style_notes'].astype(str).tolist()
        embeddings = model.encode(descriptions + [user_input], convert_to_tensor=True)
        similarities = util.pytorch_cos_sim(embeddings[-1], embeddings[:-1])[0]
        top_indices = similarities.argsort(descending=True)[:top_n * 2]
        top_matches = filtered.iloc[top_indices]
    else:
        top_matches = filtered

    # Fuzzy color match
    if color:
        top_matches_filtered = top_matches[top_matches['color'].apply(lambda c: color_match(c, color))]
        if not top_matches_filtered.empty:
            top_matches = top_matches_filtered

    return top_matches.head(top_n).to_dict(orient="records")
