import pandas as pd
import kagglehub
import os

def load_datasets():

    # Load user personality CSV
    users_df = pd.read_csv("datasets/analysis.csv")

    # Download latest Amazon reviews dataset
    path = kagglehub.dataset_download(
        "hakim11/cell-phones-and-accessories-5"
    )

    print("Path to dataset files:", path)

    # Build JSON file path
    json_path = os.path.join(
        path,
        "Cell_Phones_and_Accessories_5.json"
    )

    # Load JSONL dataset
    reviews_df = pd.read_json(
        json_path,
        lines=True
    )

    return users_df, reviews_df