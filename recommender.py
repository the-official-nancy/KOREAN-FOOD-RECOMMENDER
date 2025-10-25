
import pandas as pd
import numpy as np
from typing import List, Dict, Any

SPICY_MAP = {"None":0, "Mild":1, "Medium":2, "Hot":3}
SWEET_MAP = {"Low":0, "Medium":1, "High":2}

WEIGHTS = {
    "category": 2.0,
    "spicy": 2.0,
    "sweet": 1.0,
    "popularity": 1.0,
}

CATEGORIES = ["Rice","Stew","Noodles","Soup","BBQ","Snack/Street","Dessert","Side","Seafood"]

def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    # Normalize types
    bool_cols = [c for c in df.columns if c.startswith("contains_")] + ["vegetarian","vegan","halal_friendly"]
    for c in bool_cols:
        if c in df.columns:
            df[c] = df[c].astype(str).str.strip().str.lower().map({"true":True,"false":False,"yes":True,"no":False})
    df["spicy"] = df["spicy"].map(SPICY_MAP)
    df["sweetness"] = df["sweetness"].map(SWEET_MAP)
    df["popularity"] = pd.to_numeric(df["popularity"], errors="coerce").fillna(3).clip(1,5)
    return df

def hard_filter(df: pd.DataFrame, prefs: Dict[str, Any]) -> pd.DataFrame:
    out = df.copy()

    # Category filter (optional)
    if prefs.get("categories"):
        out = out[out["category"].isin(prefs["categories"])]

    # Dietary
    if prefs.get("vegetarian"):
        out = out[out["vegetarian"] == True]
    if prefs.get("vegan"):
        out = out[out["vegan"] == True]
    if prefs.get("halal_friendly"):
        out = out[out["halal_friendly"] == True]

    # Ingredient/allergen avoids
    for key in ["pork","beef","chicken","seafood","egg","dairy","gluten","peanuts"]:
        if prefs.get(f"avoid_{key}"):
            out = out[out[f"contains_{key}"] != True]

    return out

def soft_score(row: pd.Series, prefs: Dict[str, Any]) -> float:
    score = 0.0

    # Category match (bonus)
    if prefs.get("categories"):
        if row["category"] in prefs["categories"]:
            score += WEIGHTS["category"]

    # Spicy tolerance: prefer <= tolerance, small penalty above
    tol = prefs.get("spicy_tolerance", 3)
    if pd.notnull(row["spicy"]):
        if row["spicy"] <= tol:
            score += WEIGHTS["spicy"]
        else:
            # distance penalty
            score += max(0.0, WEIGHTS["spicy"] - 0.7*(row["spicy"] - tol))

    # Sweetness preference (optional)
    sweet_pref = prefs.get("sweet_pref")  # None, 0,1,2
    if sweet_pref is not None and pd.notnull(row["sweetness"]):
        # closer sweetness gets more
        dist = abs(row["sweetness"] - sweet_pref)
        score += max(0.0, WEIGHTS["sweet"] - 0.6*dist)

    # Popularity baseline
    score += WEIGHTS["popularity"] * (row.get("popularity", 3)/5.0)

    return score

def recommend(df: pd.DataFrame, prefs: Dict[str, Any], top_k: int = 12, sort_by: str = "score") -> pd.DataFrame:
    filtered = hard_filter(df, prefs)

    if filtered.empty:
        return filtered.assign(score=[])

    # Compute score
    scores = filtered.apply(lambda r: soft_score(r, prefs), axis=1)
    filtered = filtered.assign(score=scores)

    if sort_by == "popularity":
        filtered = filtered.sort_values(["popularity","score"], ascending=False)
    else:
        filtered = filtered.sort_values(["score","popularity"], ascending=False)

    return filtered.head(top_k)
