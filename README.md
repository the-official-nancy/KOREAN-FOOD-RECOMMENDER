
# 🍱 Korean Food Recommender (Streamlit)

A simple, polished **Korean Food Recommender** web app built with **Streamlit**. Users choose preferences
(spicy level, vegetarian/vegan/halal-friendly, dish categories, allergens, sweetness, seafood/meat choices),
and the app suggests Korean dishes with images, descriptions, and tags.

## ✨ Features
- Clean, mobile-friendly Streamlit UI
- Content-based filtering + soft scoring
- Dietary filters: **Vegetarian/Vegan/Halal-friendly**
- Allergen/ingredient filters: **pork, beef, chicken, seafood, egg, dairy, gluten, peanuts**
- Flavor filters: **Spicy tolerance** and **Sweetness**
- Categories: rice, stew, noodles, soup, bbq, snack/street, dessert, side
- Sort by score or popularity
- Dataset included (`data/foods.csv`), easy to extend

## 📦 Project Structure
```
korean-food-recommender/
├─ app_streamlit.py     # Streamlit UI
├─ recommender.py       # Filtering & scoring
├─ data/foods.csv       # Dishes dataset (editable)
├─ requirements.txt
└─ README.md
```

## 🚀 Quickstart
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app_streamlit.py
```

## 🛠️ How it works
1. Load `foods.csv` into a DataFrame.
2. Apply **hard filters** (e.g., vegetarian, halal-friendly, no pork/peanuts/gluten).
3. Apply **soft scoring** (category, spicy tolerance, sweetness, popularity).
4. Display top results with images and tags.

## 🧩 Customizing
- Add more dishes to `data/foods.csv`. Keep columns the same.
- Tweak weights in `recommender.py` (`WEIGHTS`) to emphasize different preferences.
- Replace image URLs if you have your own photos.

## 📝 License
MIT — use freely. Attribution appreciated.
