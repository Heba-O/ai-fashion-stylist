# main.py

# Import required libraries
import streamlit as st
import pandas as pd
from app.style_helpers import recommend_outfit  # Make sure the import path matches your structure

# Set the page config (must be the very first Streamlit command)
st.set_page_config(page_title="AI Fashion Stylist 👗", layout="centered")

# App title and description
st.title("👗 AI Fashion Stylist")
st.write("Get outfit suggestions based on your fashion vibe!")

# Load the outfit dataset from GitHub (cached to avoid reloading on every interaction)
@st.cache_data
def load_data():
    return pd.read_csv("https://raw.githubusercontent.com/Heba-O/ai-fashion-stylist/main/data/sample_outfits.csv")

# Load the data once
data = load_data()

# Input options - either description or filters
input_mode = st.radio("Choose input method:", ["Free-text Description", "Filters Only"])

# Description input (if selected)
user_input = ""
if input_mode == "Free-text Description":
    user_input = st.text_area("Describe your style or what you're looking for:")

# Filters - can be used with or without description
season = st.selectbox("Preferred Season (optional):", ["", "Spring", "Summer", "Autumn", "Winter", "All"])
occasion = st.selectbox("Occasion (optional):", ["", "Party", "Casual", "Formal", "Business", "Date"])
color = st.selectbox("Preferred Color (optional):", ["", "Red", "Black", "White", "Beige", "Blue", "Pink"])

# Button to trigger recommendation
if st.button("Recommend"):
    # Handle free-text or filter-based input
    if input_mode == "Free-text Description" and not user_input.strip():
        st.warning("Please enter a style description.")
    else:
        # Run the recommendation logic
        recommendations = recommend_outfit(
            user_input if input_mode == "Free-text Description" else "",
            data,
            season=season if season else None,
            occasion=occasion if occasion else None,
            color=color if color else None,
            top_n=3
        )

        # Display results if available
        if recommendations:
            st.subheader("🎯 Top Outfit Recommendations")
            for i, outfit in enumerate(recommendations, start=1):
                st.markdown(f"### 🔹 Outfit {i}")
                st.write(f"**Style:** {outfit['category']}")
                st.write(f"**Color:** {outfit['color']}")
                st.write(f"**Season:** {outfit['season']}")
                st.write(f"**Occasion:** {outfit['occasion']}")
                st.write(f"**Notes:** {outfit['style_notes']}")

                img_url = outfit.get('image_url', '')
                if img_url and isinstance(img_url, str) and img_url.startswith("http"):
                    st.image(img_url, caption=outfit['category'], use_column_width=True)
                else:
                    st.info("Image not available for this outfit.")
        else:
            st.error("No matching outfits found.")
