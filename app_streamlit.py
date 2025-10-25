import streamlit as st
import pandas as pd
import os
from recommender import load_data, recommend, CATEGORIES, SWEET_MAP, SPICY_MAP

st.set_page_config(page_title="Korean Food Recommender", page_icon="🍱", layout="wide")
st.title("🍱 Korean Food Recommender")

with st.sidebar:
    st.header("Preferences")
    categories = st.multiselect("Categories (optional)", CATEGORIES, default=[])
    spicy_label = st.select_slider("Spicy tolerance", options=list(SPICY_MAP.keys()), value="Medium")
    spicy_tolerance = SPICY_MAP[spicy_label]

    sweet_opt = st.selectbox("Sweetness preference (optional)", ["None","Low","Medium","High"], index=0)
    sweet_pref = None if sweet_opt=="None" else {"Low":0,"Medium":1,"High":2}[sweet_opt]

    st.subheader("Dietary")
    vegetarian = st.checkbox("Vegetarian only")
    vegan = st.checkbox("Vegan only")
    halal_friendly = st.checkbox("Halal-friendly only")

    st.subheader("Avoid ingredients/allergens")
    avoid_pork = st.checkbox("No pork")
    avoid_beef = st.checkbox("No beef")
    avoid_chicken = st.checkbox("No chicken")
    avoid_seafood = st.checkbox("No seafood")
    avoid_egg = st.checkbox("No egg")
    avoid_dairy = st.checkbox("No dairy")
    avoid_gluten = st.checkbox("No gluten")
    avoid_peanuts = st.checkbox("No peanuts")

    sort_by = st.radio("Sort by", ["Best match", "Popularity"], index=0)

st.caption("Tip: Start with just spicy tolerance and toggle a few avoids. Add categories to focus results.")

df = load_data("data/foods.csv")

prefs = {
    "categories": categories,
    "spicy_tolerance": spicy_tolerance,
    "sweet_pref": sweet_pref,
    "vegetarian": vegetarian,
    "vegan": vegan,
    "halal_friendly": halal_friendly,
    "avoid_pork": avoid_pork,
    "avoid_beef": avoid_beef,
    "avoid_chicken": avoid_chicken,
    "avoid_seafood": avoid_seafood,
    "avoid_egg": avoid_egg,
    "avoid_dairy": avoid_dairy,
    "avoid_gluten": avoid_gluten,
    "avoid_peanuts": avoid_peanuts,
}

top = recommend(df, prefs, top_k=12, sort_by="score" if sort_by=="Best match" else "popularity")

# Default placeholder image
DEFAULT_IMG = "https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg"

if top.empty:
    st.warning("No dishes match your filters. Try relaxing one or two constraints.")
else:
    # Display cards
    for i, row in top.iterrows():
        with st.container(border=True):
            cols = st.columns([1,2])
            with cols[0]:
                # Build local image path if available
                img_file = row["image"]
                img_path = os.path.join("images", img_file) if img_file else None

                if img_path and os.path.exists(img_path):
                    st.image(img_path, use_container_width=True)
                else:
                    st.warning("⚠️ No image available")

                st.markdown(f"**Popularity:** {int(row['popularity'])}/5")
                spicy_value = row.get("spicy", None)

                if pd.notna(spicy_value) and str(spicy_value).isdigit():
                    spicy_label = list(SPICY_MAP.keys())[int(spicy_value)]
                elif isinstance(spicy_value, str):
                    spicy_label = spicy_value 
                else:
                    spicy_label = "Unknown"

                st.markdown(f"**Spicy:** {spicy_label}")

            with cols[1]:
                st.subheader(row["name"])
                st.markdown(f"*Category:* **{row['category']}**")
                st.write(row["description"])
                tags = []
                if row.get("vegetarian"): tags.append("Vegetarian")
                if row.get("vegan"): tags.append("Vegan")
                if row.get("halal_friendly"): tags.append("Halal-friendly")
                # Ingredient tags
                for k in ["pork","beef","chicken","seafood","egg","dairy","gluten","peanuts"]:
                    if row.get(f"contains_{k}"):
                        tags.append(k.capitalize())
                if tags:
                    st.caption(" • ".join(tags))
                st.progress(min(1.0, row["score"]/6.0))
