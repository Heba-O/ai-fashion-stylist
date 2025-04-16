# main.py

# === IMPORT LIBRARIES ===
import streamlit as st  # Streamlit for building the UI
import pandas as pd  # Pandas for handling the CSV dataset
from app.style_helpers import recommend_outfit  # Custom function to get outfit recommendations

# === STREAMLIT PAGE CONFIG ===
st.set_page_config(page_title="AI Fashion Stylist 👗", layout="centered")

# === PAGE TITLE ===
st.title("👗 AI Fashion Stylist")
st.write("Get outfit suggestions based on your fashion vibe!")

# === LOAD DATA FUNCTION ===
# This function loads the CSV dataset only once (thanks to caching)
@st.cache_data
def load_data():
    return pd.read_csv("data/sample_outfits.csv")  # Make sure this path is correct

# Load the data
data = load_data()

# === USER INPUT AREA ===
# Users can describe what they are looking for
user_input = st.text_area("Describe your style or what you're looking for:")

# === OPTIONAL FILTERS ===
# Users can narrow down results using filters (optional)
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

# === RECOMMEND BUTTON ===
# When clicked, it triggers the recommendation function
if st.button("Recommend"):
    # Check if the user has typed something
    if user_input.strip():
        # Call your recommendation function with user input and selected filters
        recommended_list = recommend_outfit(
            user_input,
            data,
            season=season if season else None,
            occasion=occasion if occasion else None,
            color=color if color else None,
            top_k=3  # Return top 3 recommendations
        )

        # === DISPLAY RESULTS ===
        if recommended_list is not None:
            st.subheader("🎯 Top Outfit Matches")
            for idx, row in recommended_list.iterrows():
                st.markdown("---")  # Separator line
                st.write(f"**Style:** {row['category']}")
                st.write(f"**Color:** {row['color']}")
                st.write(f"**Season:** {row['season']}")
                st.write(f"**Occasion:** {row['occasion']}")
                st.write(f"**Notes:** {row['style_notes']}")

                # Display image if available
                if isinstance(row.get('image_url'), str) and row['image_url'].startswith("http"):
                    st.image(row['image_url'], caption=row['category'])
        else:
            st.error("No matching outfit found. Try different filters or description.")
    else:
        st.warning("Please describe your fashion style!")
