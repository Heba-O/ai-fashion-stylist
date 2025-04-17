# main.py

# Import required libraries
import streamlit as st
import pandas as pd
from app.style_helpers import recommend_outfit  # Import the outfit recommendation logic

# Set the page config
st.set_page_config(page_title="AI Fashion Stylist 👗", layout="centered")

# App title and description
st.title("👗 AI Fashion Stylist")
st.write("Describe your fashion vibe or select filters to get AI-powered outfit recommendations!")

# Load the outfit dataset from GitHub
@st.cache_data
def load_data():
    return pd.read_csv("https://raw.githubusercontent.com/Heba-O/ai-fashion-stylist/main/data/sample_outfits.csv")

# Load the dataset
data = load_data()

# --- UI Control: Mode Selection ---
mode = st.radio("Choose your recommendation method:", ["Use Style Description", "Choose by Filters Only"])

# --- Optional Slider for number of outfit suggestions ---
num_suggestions = st.slider("How many outfits would you like to see?", 1, 5, 3)

# --- Get user input ---
user_input = ""
season = occasion = color = None

if mode == "Use Style Description":
    user_input = st.text_area("Describe your style or what you're looking for (e.g., 'cozy autumn outfit with a scarf'):")
else:
    season = st.selectbox("Preferred Season (optional):", ["", "Spring", "Summer", "Autumn", "Winter", "All"])
    occasion = st.selectbox("Occasion (optional):", ["", "Party", "Casual", "Formal", "Business", "Date"])
    color = st.selectbox("Preferred Color (optional):", ["", "Red", "Black", "White", "Beige", "Blue", "Pink"])

# --- Recommend Button ---
if st.button("Recommend"):
    if mode == "Use Style Description" and not user_input.strip():
        st.warning("Please describe your fashion style!")
    else:
        recommendations = recommend_outfit(
            user_input,
            data,
            top_k=num_suggestions,
            season=season if season else None,
            occasion=occasion if occasion else None,
            color=color if color else None
        )

        if not recommendations.empty:
            st.subheader("🌟 Top Outfit Recommendations")
            for i, (_, outfit) in enumerate(recommendations.iterrows(), 1):
                with st.container():
                    st.markdown(f"### 🔹 Outfit {i}")
                    img_url = outfit.get("image_url", "")
                    if img_url and isinstance(img_url, str) and img_url.startswith("http") and (img_url.endswith(".jpg") or img_url.endswith(".png")):
                        st.image(img_url, caption=outfit['category'], use_column_width=True)
                    else:
                        st.image("https://via.placeholder.com/300x400?text=No+Image", caption="Image unavailable", use_column_width=True)

                    st.markdown(f"**Style:** {outfit['category']}")
                    st.markdown(f"**Color:** {outfit['color']}")
                    st.markdown(f"**Season:** {outfit['season']}")
                    st.markdown(f"**Occasion:** {outfit['occasion']}")
                    st.markdown(f"**Notes:** {outfit['style_notes']}")
                    st.markdown("---")
        else:
            st.error("Sorry, no matching outfits found with the selected filters or description.")
