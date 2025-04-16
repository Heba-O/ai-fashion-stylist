# app/style_helpers.py

# === IMPORT LIBRARIES ===
from sentence_transformers import SentenceTransformer, util  # For encoding text and measuring similarity
import pandas as pd  # For handling DataFrame operations

# === LOAD PRETRAINED LANGUAGE MODEL ===
# This model turns text into vector embeddings for similarity comparison
# 'all-MiniLM-L6-v2' is lightweight and works well for semantic search
model = SentenceTransformer('all-MiniLM-L6-v2')

# === RECOMMENDATION FUNCTION ===
def recommend_outfit(user_input, data, season=None, occasion=None, color=None, top_k=3):
    """
    Recommend the top_k outfits that best match the user's text input and optional filters.
    
    Parameters:
    - user_input: str, natural language input from the user
    - data: DataFrame, the outfit dataset
    - season, occasion, color: optional filters to narrow down choices
    - top_k: number of top recommendations to return
    
    Returns:
    - DataFrame with top matching outfit rows
    """
    
    # Copy the dataset so original data stays unchanged
    filtered = data.copy()

    # === APPLY FILTERS (IF ANY) ===
    if season:
        filtered = filtered[filtered['season'].str.lower() == season.lower()]
    if occasion:
        filtered = filtered[filtered['occasion'].str.lower() == occasion.lower()]
    if color:
        filtered = filtered[filtered['color'].str.lower() == color.lower()]

    # === IF NO MATCH AFTER FILTERING ===
    if filtered.empty:
        return None

    # === ENCODE TEXT TO VECTORS ===
    # Get the style notes for outfits (as a list of strings)
    style_notes = filtered['style_notes'].astype(str).tolist()

    # Convert all outfit descriptions + user input into embeddings (vectors)
    embeddings = model.encode(style_notes, convert_to_tensor=True)
    user_embedding = model.encode(user_input, convert_to_tensor=True)

    # === COMPUTE SIMILARITY SCORES ===
    # Compare the user input with each outfit's style notes
    cosine_scores = util.cos_sim(user_embedding, embeddings)[0]

    # Get the indices of the top-k most similar outfits
    top_results = cosine_scores.argsort(descending=True)[:top_k]

    # Return the top matching outfits from the filtered dataset
    return filtered.iloc[top_results]
