# style_helpers.py
import pandas as pd
from sentence_transformers import SentenceTransformer, util
from fuzzywuzzy import fuzz, process
import torch

# Load model once
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_semantic_matches(user_input, data, top_n=3):
    # Combine relevant fields for semantic search
    data = data.copy()
    data["combined"] = (
        data["style_notes"].fillna("") + " " +
        data["category"].fillna("") + " " +
        data["season"].fillna("") + " " +
        data["occasion"].fillna("") + " " +
        data["color"].fillna("")
    )

    descriptions = data['combined'].tolist()
    query_embedding = model.encode(user_input, convert_to_tensor=True)
    passage_embeddings = model.encode(descriptions, convert_to_tensor=True)
    scores = util.pytorch_cos_sim(query_embedding, passage_embeddings)[0]
    top_results = torch.topk(scores, k=top_n * 3)  # get more candidates for reranking
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
        reranked = []
        for idx, sim_score in matches:
            outfit = data.iloc[idx]
            score = sim_score
            if season and fuzz.partial_ratio(season.lower(), outfit['season'].lower()) > 70:
                score += 0.3
            if occasion and fuzz.partial_ratio(occasion.lower(), outfit['occasion'].lower()) > 70:
                score += 0.3
            if color and fuzz.partial_ratio(color.lower(), outfit['color'].lower()) > 70:
                score += 0.3
            reranked.append((idx, score))

        reranked = sorted(reranked, key=lambda x: x[1], reverse=True)[:top_n]
        recommendations = [data.iloc[idx].to_dict() for idx, _ in reranked]
        return recommendations

    else:
        filtered = data.copy()
        if season:
            filtered = filter_by_fuzzy_match(filtered, 'season', season)
        if occasion:
            filtered = filter_by_fuzzy_match(filtered, 'occasion', occasion)
        if color:
            filtered = filter_by_fuzzy_match(filtered, 'color', color)

        if filtered.empty:
            return []

        # Score and rank by fuzzy similarity
        scored = []
        for i, row in filtered.iterrows():
            score = 0
            if season:
                score += fuzz.partial_ratio(season.lower(), str(row['season']).lower()) / 100
            if occasion:
                score += fuzz.partial_ratio(occasion.lower(), str(row['occasion']).lower()) / 100
            if color:
                score += fuzz.partial_ratio(color.lower(), str(row['color']).lower()) / 100
            scored.append((row.to_dict(), score))

        scored = sorted(scored, key=lambda x: x[1], reverse=True)[:top_n]
        return [rec for rec, _ in scored]
