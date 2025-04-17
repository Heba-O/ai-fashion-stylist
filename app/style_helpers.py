import pandas as pd
from sentence_transformers import SentenceTransformer, util
from fuzzywuzzy import process

# Load the model globally
model = SentenceTransformer("all-MiniLM-L6-v2")

def flexible_filter_match(row_value, user_value, threshold=80):
    """
    Apply fuzzy matching to a field value and user preference.
    """
    if not user_value:
        return True  # If user did not select a filter, allow all values
    if pd.isna(row_value):
        return False
    best_match = process.extractOne(user_value.lower(), [row_value.lower()])
    if best_match:
        _, score = best_match
        return score >= threshold
    return False

def recommend_outfit(user_input, data, season=None, occasion=None, color=None, top_n=3):
    """
    Recommend top N outfits using filter + semantic similarity.
    """
    filtered = data.copy()

    # Apply flexible fuzzy filters
    if season:
        filtered = filtered[filtered['season'].apply(lambda x: flexible_filter_match(x, season))]
    if occasion:
        filtered = filtered[filtered['occasion'].apply(lambda x: flexible_filter_match(x, occasion))]
    if color:
        filtered = filtered[filtered['color'].apply(lambda x: flexible_filter_match(x, color))]

    # If using free-text input, apply semantic similarity
    if user_input.strip():
        descriptions = filtered['style_notes'].tolist()
        if not descriptions:
            return []
        embeddings = model.encode(descriptions + [user_input], convert_to_tensor=True)
        similarities = util.pytorch_cos_sim(embeddings[-1], embeddings[:-1])[0]
        top_indices = similarities.argsort(descending=True)[:top_n * 2]
        filtered = filtered.iloc[top_indices]

    return filtered.head(top_n).to_dict(orient="records")
