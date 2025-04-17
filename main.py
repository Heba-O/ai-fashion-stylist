# main.py
import streamlit as st
import pandas as pd
from app.style_helpers import recommend_outfit
from PIL import Image
import requests
from io import BytesIO

# Configure the Streamlit page
st.set_page_config(page_title="AI Fashion Stylist 👗", layout="centered")

# Title and description
st.title("👗 AI Fashion Stylist")
st.write("Get AI-powered outfit recommendations based on your style or filters!")

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("https://raw.githubusercontent.com/Heba-O/ai-fashion-stylist/main/data/sample_outfits.csv")

data = load_data()

# Function to safely display images from URLs
def safe_display_image(img_url, caption):
    if not img_url:
        st.warning("⚠️ Image could not be loaded (URL is missing).")
        return
    try:
        response = requests.get(img_url)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            st.image(img, caption=caption, use_container_width=True)
        else:
            st.warning("⚠️ Image could not be loaded (URL is broken).")
    except Exception:
        st.warning("⚠️ Image could not be loaded (Invalid URL or network issue).")

# Input method selection
input_method = st.radio("Choose input method:", ["Free-text Description", "Filters Only"])

user_input = ""
season = occasion = color = None

# Handle input based on method
if input_method == "Free-text Description":
    user_input = st.text_area("Describe your style or what you're looking for:")
    st.caption("Example: 'Want a cozy red casual outfit for an autumn picnic'")
else:
    st.markdown("#### Filters:")
    season = st.selectbox("Preferred Season:", ["", "Spring", "Summer", "Autumn", "Winter", "All"])
    occasion = st.selectbox("Occasion:", ["", "Party", "Casual", "Formal", "Business", "Date"])
    color = st.selectbox("Preferred Color:", ["", "Red", "Black", "White", "Beige", "Blue", "Pink"])

# Recommend button
if st.button("Recommend"):
    if input_method == "Free-text Description" and not user_input.strip():
        st.warning("Please describe your fashion style!")
    else:
        recommendations = recommend_outfit(
            user_input=user_input if input_method == "Free-text Description" else "",
            data=data,
            season=season if season else None,
            occasion=occasion if occasion else None,
            color=color if color else None,
            top_n=3
        )

        if recommendations:
            st.subheader("🎯 Top Outfit Recommendations")
            for idx, rec in enumerate(recommendations):
                st.markdown(f"### 🔹 Outfit {idx + 1}")
                st.write(f"**Style:** {rec['category']}")
                st.write(f"**Color:** {rec['color']}")
                st.write(f"**Season:** {rec['season']}")
                st.write(f"**Occasion:** {rec['occasion']}")
                st.write(f"**Notes:** {rec['style_notes']}")
                img_url = rec.get("image_url", "")
                safe_display_image(img_url, rec['category'])
        else:
            st.error("No matching outfits found. Try adjusting your description or filters.")

