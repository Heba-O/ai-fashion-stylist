# main.py

import streamlit as st
import pandas as pd
from app.style_helpers import recommend_outfit

# ✅ Must be at the very top!
st.set_page_config(page_title="AI Fashion Stylist 👗", layout="centered")

st.title("👗 AI Fashion Stylist")
st.write("Get outfit suggestions based on your fashion vibe!")

@st.cache_data
def load_data():
    return pd.read_csv("https://raw.githubusercontent.com/Heba-O/ai-fashion-stylist/main/data/sample_outfits.csv")

data = load_data()

user_input = st.text_area("Describe your style or what you're looking for:")

# Optional filters
season_filter = st.selectbox("Preferred Season:", ["Any"] + sorted(data['season'].dropna().unique()))
occasion_filter = st.selectbox("Occasion:", ["Any"] + sorted(data['occasion'].dropna().unique()))
color_filter = st.selectbox("Preferred Color:", ["Any"] + sorted(data['color'].dropna().unique()))

if st.button("Recommend"):
    if user_input.strip():
        recommended = recommend_outfit(user_input, data, season_filter, occasion_filter, color_filter)

        st.subheader("🎯 Recommended Outfit")
        st.write(f"**Category (Style):** {recommended['category']}")
        st.write(f"**Color:** {recommended['color']}")
        st.write(f"**Season:** {recommended['season']}")
        st.write(f"**Occasion:** {recommended['occasion']}")
        st.write(f"**Notes:** {recommended['style_notes']}")

        # Use placeholder image if image_url is invalid
        img_url = recommended['image_url']
        if not str(img_url).startswith("http"):
            img_url = f"https://via.placeholder.com/150?text={recommended['category']}"

        st.image(img_url, caption=recommended['category'])
    else:
        st.warning("Please describe your fashion style!")
