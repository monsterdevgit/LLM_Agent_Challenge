import streamlit as st
import pandas as pd

from helpers.config import get_client
from helpers.data_loader import load_datasets
from models.user_profiles import build_synthetic_user
from prediction.llm_simulator import simulate_user_response


# Load data (cache for speed)
@st.cache_data
def load_data():
    return load_datasets()


# App title
st.title("Personality-Aware Review Simulation")
st.write("Simulate how a user would review a product based on personality traits")


# Load datasets
users_df, reviews_df = load_data()

# LLM client
client = get_client()


# USER SELECTION
st.header("Select User Persona")

user_id = st.selectbox(
    "Choose a user",
    users_df["usuario"]
)

# Get selected user row
user_row = users_df[users_df["usuario"] == user_id].iloc[0]


# PRODUCT INPUT
st.header("Product Description")

product = st.text_area(
    "Enter product details",
    "Wireless Bluetooth headphones with noise cancellation"
)


# BUTTON
if st.button("Generate Review"):

    with st.spinner("Simulating user behavior..."):

        # Build synthetic user
        user_features, history = build_synthetic_user(user_row, reviews_df)

        # Generate prediction
        prediction = simulate_user_response(
            client,
            user_features,
            history,
            product
        )

    # DISPLAY OUTPUT
    if prediction:

        st.success("Simulation Complete")

        st.subheader(" Predicted Rating")
        st.markdown(f"### {prediction['Score']} / 5")

        st.subheader(" Generated Review")
        st.write(prediction["Review"])

    else:
        st.error("Failed to generate prediction")


#  SHOW USER INFO
with st.expander(" User Personality Details"):
    st.write(user_row.to_dict())