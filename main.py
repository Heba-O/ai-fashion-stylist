import streamlit as st
import pandas as pd
from app.style_helpers import recommend_outfit
from PIL import Image
import requests
from io import BytesIO

st.set_page_config(page_title="AI Fashion Stylist", layout="wide")
st.title("👗 AI Fashion Stylist")

# Load data
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/Heba-O/ai-fashion-stylist/refs/heads/main/data/sample_outfits.csv"
    return pd.read_csv(url)

data = load_data()

# Dropdown values
seasons = sorted(data["season"].dropna().unique().tolist())
occasions = sorted(data["occasion"].dropna().unique().tolist())
colors = sorted(data["color"].dropna().unique().tolist())

# Input method
input_method = st.radio("Choose Input Method:", ["Free-text Description", "Filter Selection"])

user_input = ""
season = occasion = color = None

if input_method == "Free-text Description":
    user_input = st.text_area("Describe your style or what you're looking for:")
    st.caption("Example: 'Looking for a cozy red outfit for an autumn picnic'")
else:
    season = st.selectbox("Preferred Season:", [""] + seasons)
    occasion = st.selectbox("Occasion:", [""] + occasions)
    color = st.selectbox("Preferred Color:", [""] + colors)

# Image display
def safe_display_image(url, alt):
    try:
        response = requests.get(url, timeout=5)
        img = Image.open(BytesIO(response.content))
        st.image(img, caption=alt, use_column_width=True)
    except Exception:
        st.warning("⚠️ Image could not be loaded (URL is broken).")

# Recommend button
if st.button("Recommend"):
    if input_method == "Free-text Description" and not user_input.strip():
        st.warning("Please enter a description!")
    else:
        recommendations = recommend_outfit(
            user_input=user_input if input_method == "Free-text Description" else "",
            data=data,
            season=season if input_method == "Filter Selection" else None,
            occasion=occasion if input_method == "Filter Selection" else None,
            color=color if input_method == "Filter Selection" else None,
            top_n=3
        )
        if recommendations:
            st.subheader("🎯 Top Outfit Recommendations")
            for i, rec in enumerate(recommendations):
                st.markdown(f"### 🔹 Outfit {i + 1}")
                st.write(f"**category:** {rec.get('category', 'N/A')}")
                st.write(f"**Color:** {rec.get('color', 'N/A')}")
                st.write(f"**Season:** {rec.get('season', 'N/A')}")
                st.write(f"**Occasion:** {rec.get('occasion', 'N/A')}")
                st.write(f"**Notes:** {rec.get('style_notes', '')}")
                safe_display_image(rec.get("image_url", ""), rec.get("category", "Outfit"))
        else:
            st.error("No matching outfits found. Try adjusting your description or filters.")
