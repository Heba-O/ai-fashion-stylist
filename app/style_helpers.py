# app/style_helpers.py

from sentence_transformers import SentenceTransformer, util  # Semantic similarity
import pandas as pd  # Data handling

# === LOAD TRANSFORMER MODEL ===
# This model turns text into meaningful vector embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')

def recommend_outfit(user_input, data, season=None, occasion=None, color=None, top_k=3):
    """
    Recommend the top_k outfits based on user description and optional filters.

    Parameters:
        user_input (str): User's fashion description
        data (pd.DataFrame): Outfit dataset
        season, occasion, color (str, optional): Filter options
        top_k (int): Number of outfits to return

    Returns:
        pd.DataFrame: Top matching outfits
    """
    
    # Step 1: Encode all outfit style notes
    style_notes = data['style_notes'].astype(str).tolist()
    outfit_embeddings = model.encode(style_notes, convert_to_tensor=True)

    # Step 2: Encode user input
    user_embedding = model.encode(user_input, convert_to_tensor=True)

    # Step 3: Calculate cosine similarity between user input and all outfits
    similarity_scores = util.cos_sim(user_embedding, outfit_embeddings)[0]

    # Step 4: Pick top 10 semantically similar results
    top_indices = similarity_scores.argsort(descending=True)[:10]
    top_matches = data.iloc[top_indices].copy()

    # Step 5: Apply optional filters on top matches
    if season:
        top_matches = top_matches[top_matches['season'].str.lower() == season.lower()]
    if occasion:
        top_matches = top_matches[top_matches['occasion'].str.lower() == occasion.lower()]
    if color:
        top_matches = top_matches[top_matches['color'].str.lower() == color.lower()]

    # Step 6: Fallback to top similar items if filters remove everything
    if top_matches.empty:
        return data.iloc[top_indices[:top_k]]

    # Step 7: Return top-k results
    return top_matches.head(top_k)
