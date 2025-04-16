# main.py

import streamlit as st
import pandas as pd

# ✅ Must be at the very top!
st.set_page_config(page_title="AI Fashion Stylist 👗", layout="centered")

# ✅ Now that we're outside `app/`, we can import this way
from app.style_helpers import recommend_outfit

st.title("👗 AI Fashion Stylist")
st.write("Get outfit suggestions based on your fashion vibe!")

@st.cache_data
def load_data():
    return pd.read_csv("https://raw.githubusercontent.com/Heba-O/ai-fashion-stylist/main/data/sample_outfits.csv")

data = load_data()

user_input = st.text_area("Describe your style or what you're looking for:")

if st.button("Recommend"):
    if user_input.strip():
        recommended = recommend_outfit(user_input, data)

        st.subheader("🎯 Recommended Outfit")
        st.write(f"**Style:** {recommended['style']}")
        st.write(f"**Notes:** {recommended['style_notes']}")
    else:
        st.warning("Please describe your fashion style!")
