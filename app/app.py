# app/app.py

import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="AI Fashion Stylist 👗", layout="centered")

st.title("👗 AI Fashion Stylist")
st.write("Get outfit suggestions based on your fashion vibe!")

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("https://raw.githubusercontent.com/Heba-O/ai-fashion-stylist/main/data/sample_outfits.csv")

data = load_data()

# User input
user_input = st.text_area("Describe your style or what you're looking for:")

if st.button("Recommend"):
    if user_input.strip() != "":
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(data["style_notes"].astype(str).tolist() + [user_input])
        cosine_sim = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
        top_index = cosine_sim[0].argsort()[-1]
        recommended = data.iloc[top_index]

        st.subheader("🎯 Recommended Outfit")
        st.write(f"**Style:** {recommended['style']}")
        st.write(f"**Notes:** {recommended['style_notes']}")
    else:
        st.warning("Please describe your fashion style!")
