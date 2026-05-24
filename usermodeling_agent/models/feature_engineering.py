import pandas as pd


def build_user_features(users_df):
    return users_df.copy()


def build_review_features(reviews_df):

    # average score per user
    user_stats = reviews_df.groupby("reviewerID").agg({
        "overall": ["mean", "count"]
    })

    user_stats.columns = ["avg_score", "review_count"]

    return user_stats.reset_index()


def build_feature_dataset(users_df, reviews_df):

    user_features = build_user_features(users_df)
    review_features = build_review_features(reviews_df)

    # merge
    df = user_features.merge(
        review_features,
        left_on="usuario",
        right_on="reviewerID",
        how="left"
    )

    df.fillna(0, inplace=True)

    return df
