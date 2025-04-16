# main.py

# Import required libraries
import streamlit as st
import pandas as pd
from app.style_helpers import recommend_outfit  # Import the outfit recommendation logic

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

# User input for free-text description (e.g., "I want a red outfit for a summer date")
user_input = st.text_area("Describe your style or what you're looking for:")

# Optional filters for more precise recommendations
season = st.selectbox(
    "Preferred Season (optional):",
    ["", "Spring", "Summer", "Autumn", "Winter", "All"]
)

occasion = st.selectbox(
    "Occasion (optional):",
    ["", "Party", "Casual", "Formal", "Business", "Date"]
)

color = st.selectbox(
    "Preferred Color (optional):",
    ["", "Red", "Black", "White", "Beige", "Blue", "Pink"]
)

# Button to trigger outfit recommendation
if st.button("Recommend"):
    if user_input.strip():  # Make sure the user typed something
        # Call the recommendation function with filters (if selected)
        recommended = recommend_outfit(
            user_input,
            data,
            season=season if season else None,
            occasion=occasion if occasion else None,
            color=color if color else None
        )

        # Display the recommended outfit if found
        if recommended is not None:
            st.subheader("🎯 Recommended Outfit")
            st.write(f"**Category (Style):** {recommended['category']}")
            st.write(f"**Color:** {recommended['color']}")
            st.write(f"**Season:** {recommended['season']}")
            st.write(f"**Occasion:** {recommended['occasion']}")
            st.write(f"**Notes:** {recommended['style_notes']}")
            img_url = recommended.get('image_url', '')
if img_url and isinstance(img_url, str) and img_url.startswith("http"):
    st.image(img_url, caption=recommended['category'])
else:
    st.info("No image available for this outfit.")

        else:
            st.error("Sorry, no matching outfits found with the selected filters.")
    else:
        st.warning("Please describe your fashion style!")
