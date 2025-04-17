# style_helpers.py
import pandas as pd
from sentence_transformers import SentenceTransformer, util
from fuzzywuzzy import fuzz, process
import torch

# Load model once
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_semantic_matches(user_input, data, top_n=3):
    descriptions = data['style_notes'].fillna("").tolist()
    query_embedding = model.encode(user_input, convert_to_tensor=True)
    passage_embeddings = model.encode(descriptions, convert_to_tensor=True)
    scores = util.pytorch_cos_sim(query_embedding, passage_embeddings)[0]
    top_results = torch.topk(scores, k=top_n)
    return [(int(idx), float(scores[idx])) for idx in top_results.indices]

def filter_by_fuzzy_match(df, column, value):
    if not value or df.empty or column not in df.columns:
        return df

    choices = df[column].dropna().unique().tolist()
    if not choices:
        return df

    result = process.extractOne(value.lower(), choices)
    if result is None:
        return df

    best_match, score = result
    if score < 60:
        return df[0:0]  # Return empty DataFrame

    return df[df[column].str.lower() == best_match.lower()]

def recommend_outfit(user_input=None, season=None, occasion=None, color=None, top_n=3, data=None):
    if data is None:
        return []

    if user_input:
        matches = get_semantic_matches(user_input, data, top_n=top_n)
        for i, (idx, score) in enumerate(matches):
            outfit = data.iloc[idx]
            if season and fuzz.partial_ratio(season.lower(), outfit['season'].lower()) > 70:
                score += 0.1
            if occasion and fuzz.partial_ratio(occasion.lower(), outfit['occasion'].lower()) > 70:
                score += 0.1
            if color and fuzz.partial_ratio(color.lower(), outfit['color'].lower()) > 70:
                score += 0.1
            matches[i] = (idx, score)

        matches = sorted(matches, key=lambda x: x[1], reverse=True)[:top_n]
        recommendations = [data.iloc[idx] for idx, _ in matches]
        return recommendations

    else:
        filtered = data
        if season:
            filtered = filter_by_fuzzy_match(filtered, 'season', season)
        if occasion:
            filtered = filter_by_fuzzy_match(filtered, 'occasion', occasion)
        if color:
            filtered = filter_by_fuzzy_match(filtered, 'color', color)

        if len(filtered) == 0:
            return []

        return filtered.sample(n=min(top_n, len(filtered))).to_dict(orient='records')
