# main.py

# Import required libraries
import streamlit as st
import pandas as pd
from app.style_helpers import recommend_outfits  # Updated import

# Set Streamlit page config
st.set_page_config(page_title="AI Fashion Stylist 👗", layout="centered")

# App title and instructions
st.title("👗 AI Fashion Stylist")
st.write("Describe your fashion vibe and get personalized outfit recommendations!")

# Load dataset from GitHub (cached for performance)
@st.cache_data
def load_data():
    return pd.read_csv("https://raw.githubusercontent.com/Heba-O/ai-fashion-stylist/main/data/sample_outfits.csv")

# Load data once at app startup
data = load_data()

# User input: free-text description
user_input = st.text_area("Describe your style or what you're looking for (e.g., 'cozy autumn outfit with a scarf'):")

# Optional filters
season = st.selectbox(
    "Preferred Season (optional):",
    ["", "Spring", "Summer", "Autumn", "Winter"]
)

occasion = st.selectbox(
    "Occasion (optional):",
    ["", "Casual", "Date", "Party", "Formal", "Business"]
)

color = st.selectbox(
    "Preferred Color (optional):",
    ["", "Red", "Black", "White", "Beige", "Blue", "Pink", "Gray", "Brown", "Yellow", "Green", "Purple", "Orange", "Teal", "Cream"]
)

# Recommend button logic
if st.button("Recommend"):
    if user_input.strip():
        # Call the updated function to get top 3 recommendations
        recommendations = recommend_outfits(
            user_input,
            data,
            season=season if season else None,
            occasion=occasion if occasion else None,
            color=color if color else None
        )

        # Display results
        if recommendations:
            st.subheader("🎯 Top Outfit Recommendations")
            for i, outfit in enumerate(recommendations, 1):
                st.markdown(f"### 🔹 Outfit {i}")
                st.write(f"**Style:** {outfit['category']}")
                st.write(f"**Color:** {outfit['color']}")
                st.write(f"**Season:** {outfit['season']}")
                st.write(f"**Occasion:** {outfit['occasion']}")
                st.write(f"**Notes:** {outfit['style_notes']}")
                
                # Display image if valid
                img_url = outfit.get('image_url', '')
                if img_url and isinstance(img_url, str) and img_url.startswith("http"):
                    st.image(img_url, caption=outfit['category'])
                st.markdown("---")
        else:
            st.error("No matching outfits found. Try adjusting your filters or description.")
    else:
        st.warning("Please enter a fashion description to get recommendations.")
