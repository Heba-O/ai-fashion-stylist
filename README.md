# 👗 AI Fashion Stylist

> Your intelligent personal stylist — powered by AI and trained to recommend stunning, personalized outfit ideas based on mood, occasion, and style preferences.

---

## 🌟 Project Overview

The AI Fashion Stylist is a smart assistant designed to elevate your wardrobe choices using machine learning and computer vision. Whether you’re dressing for a date, a job interview, or a casual brunch, this app suggests fashion-forward looks tailored just for you.

---

## 🧠 Features

- 🎨 Analyze outfit images and generate style descriptions
- 📅 Suggest outfits based on occasion, season, and user mood
- 🧍‍♀️ Personalize fashion recommendations using user profile data
- 🤖 AI-powered recommendations using vision & NLP models
- 🛍️ Optional styling add-ons from public fashion datasets

---

## 📂 Project Structure

---

## 📊 Dataset

This project uses curated outfit datasets containing:
- Image URLs and outfit descriptions
- Fashion tags and color palettes
- Occasion and seasonal labels

(*Dataset upload in progress — stay tuned!*)

---

## 🧪 Model Development

Initial prototype leverages:
- **Vision Models** (e.g., MobileNet, CLIP) to understand outfit images
- **Text Embedding Models** (e.g., BERT, GPT-based) to analyze preferences
- Cosine similarity and KNN for outfit matching and recommendations

Notebook: [`model_dev.ipynb`](./model_dev.ipynb)

---

## 🚀 Getting Started

To run this project locally:

```bash
# Clone the repository
git clone https://github.com/Heba-O/ai-fashion-stylist.git

# Navigate to the project folder
cd ai-fashion-stylist

# Install requirements (coming soon)
pip install -r requirements.txt

##colab badge
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Heba-O/ai-fashion-stylist/blob/main/notebooks/model_dev.ipynb)

