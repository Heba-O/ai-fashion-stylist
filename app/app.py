# app/app.py

import sys
import os

# Add parent dir to sys.path before any local imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd

# Set Streamlit config FIRST before any other Streamlit command
st.set_page_config(page_title="AI Fashion Stylist 👗", layout="centered")

# Now import local modules
from app.style_helpers import recommend_outfit

# App UI
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
        recommended = recommend_outfit(user_input, data)

        st.subheader("🎯 Recommended Outfit")
        st.write(f"**Style:** {recommended['style']}")
        st.write(f"**Notes:** {recommended['style_notes']}")
    else:
        st.warning("Please describe your fashion style!")
