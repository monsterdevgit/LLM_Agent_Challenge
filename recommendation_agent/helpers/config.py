import os
import google.generativeai as genai
import weaviate
from weaviate.auth import AuthApiKey
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


# GEMINI SETUP
def get_model():
    api_key = os.getenv("API-Key")

    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in .env")

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-2.0-flash")

    return model


# WEAVIATE SETUP
def get_client():
    url = os.getenv("WEAVIATE_URL")
    api_key = os.getenv("WEAVIATE_API_KEY")

    if not url or not api_key:
        raise ValueError("❌ Missing Weaviate credentials in .env")

    client = weaviate.connect_to_weaviate_cloud(
        cluster_url=url,
        auth_credentials=AuthApiKey(api_key),
    )

    return client


# GET PRODUCTS COLLECTION
def get_products_collection(client):
    return client.collections.get("Products")