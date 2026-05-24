def get_user_data(user_id, users_df, reviews_df):

    user_row = users_df[users_df["usuario"] == user_id]

    if user_row.empty:
        return None, None

    user_features = user_row.iloc[0].to_dict()

    user_reviews = reviews_df[reviews_df["reviewerID"] == user_id]

    review_history = user_reviews[["reviewText", "overall"]].to_dict("records")

    return user_features, review_history[:5]


def personality_to_style(user):

    traits = []

    if user["ex"] > 40:
        traits.append("expressive and energetic")

    if user["ne"] > 10:
        traits.append("critical and sensitive")

    if user["co"] > 25:
        traits.append("structured and detail-oriented")

    return ", ".join(traits) if traits else "balanced"