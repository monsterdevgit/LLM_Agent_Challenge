import pandas as pd


# ✅ Personality → behavior filter
def filter_reviews(user, reviews_df):

    if user["ne"] > 30:
        return reviews_df[reviews_df["overall"] <= 3]

    if user["ag"] > 30:
        return reviews_df[reviews_df["overall"] >= 4]

    return reviews_df


# ✅ Match writing length
def filter_by_length(user, df):

    target_len = user.get("wordcount", 50)

    df = df.copy()
    df["length"] = df["reviewText"].astype(str).str.len()

    return df[
        (df["length"] > target_len * 10) &
        (df["length"] < target_len * 100)
    ]


# ✅ Final smart sampling
def get_smart_history(user, reviews_df, n=5):

    # ✅ use both filters
    filtered = filter_reviews(user, reviews_df)
    filtered = filter_by_length(user, filtered)

    # ✅ fallback if filtering too strict
    if filtered.empty:
        filtered = reviews_df.sample(200)

    return filtered.sample(n)[["reviewText", "overall"]].to_dict("records")


# ✅ MAIN FUNCTION (used in main.py)
def build_synthetic_user(row, reviews_df):

    user_features = row.to_dict()

    history = get_smart_history(user_features, reviews_df)

    return user_features, history