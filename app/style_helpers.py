# style_helpers.py
import pandas as pd
from sentence_transformers import SentenceTransformer, util
from fuzzywuzzy import process

model = SentenceTransformer('all-MiniLM-L6-v2')

def filter_by_fuzzy_match(df, column, value, threshold=70):
    if not value:
        return df
    choices = df[column].dropna().unique()
    match = process.extractOne(value.lower(), choices)
    if match and match[1] >= threshold:
        best_match = match[0]
        return df[df[column].str.lower() == best_match.lower()]
    return df  # Fallback: return unfiltered if no good match

def recommend_outfit(df, user_input="", season=None, occasion=None, color=None, top_n=3):
    # If description is given, use semantic search
    if user_input:
        embeddings = model.encode(df['style_notes'].tolist(), convert_to_tensor=True)
        query_embedding = model.encode(user_input, convert_to_tensor=True)
        cos_scores = util.pytorch_cos_sim(query_embedding, embeddings)[0]

        df['score'] = cos_scores.cpu().numpy()

        # Boost score for matching filters
        def boost_score(row):
            boost = 0
            if season and season.lower() in str(row['season']).lower():
                boost += 0.15
            if occasion and occasion.lower() in str(row['occasion']).lower():
                boost += 0.15
            if color and color.lower() in str(row['color']).lower():
                boost += 0.15
            return row['score'] + boost

        df['boosted_score'] = df.apply(boost_score, axis=1)
        return df.sort_values(by='boosted_score', ascending=False).head(top_n)

    # If using filters only
    filtered = df.copy()
    filtered = filter_by_fuzzy_match(filtered, 'season', season)
    filtered = filter_by_fuzzy_match(filtered, 'occasion', occasion)
    filtered = filter_by_fuzzy_match(filtered, 'color', color)

    return filtered.head(top_n)
