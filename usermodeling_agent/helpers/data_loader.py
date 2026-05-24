import pandas as pd

def load_datasets():

    # ✅ Load CSV
    users_df = pd.read_csv("datasets/analysis.csv")

    # ✅ Load JSONL (Amazon dataset)
    reviews_df = pd.read_json(
        "datasets/Cell_Phones_and_Accessories_5.json",
        lines=True
    )

    return users_df, reviews_df