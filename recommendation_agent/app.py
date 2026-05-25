import streamlit as st

st.write("App is loading...")

from helpers.config import get_model, get_client, get_products_collection

#  Initialize
model = get_model()
client = get_client()
products = get_products_collection(client)

# Import your agent functions
from helpers.memory import update_memory, user_profile, store_feedback
from helpers.planner import planner
from helpers.retrieval import retrieve_products
from helpers.reranker import rerank
from helpers.generator import generate_response


# Agent pipeline
def agent_chat(user_input):

    profile = update_memory(model, user_input)
    print("PROFILE:", profile)

    plan = planner(model, user_input, profile)
    print("PLAN:", plan)

    results = retrieve_products(
        products,
        plan["search_query"],
        plan.get("category")
    )

    print("RESULT COUNT:", len(results))

    ranked = rerank(model, user_input, results)
    print("RANKED COUNT:", len(ranked))

    response = generate_response(model, user_input, ranked, profile)

    return response, ranked[:5]


# Streamlit UI
st.set_page_config(page_title="AI Product Recommender Agent", layout="wide")

st.title("AI Amazon Recommendation Agent")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Input
user_input = st.chat_input("Ask for products...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    response, items = agent_chat(user_input)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response,
        "products": items
    })


# Display chat
for msg in st.session_state.messages:

    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])

    else:
        st.chat_message("assistant").write(msg["content"])

        # Show products nicely
        if "products" in msg:
            cols = st.columns(5)

            for i, item in enumerate(msg["products"]):
                with cols[i]:
                    st.image(item.properties["image"], use_container_width=True)
                    st.write(item.properties["name"])
                    st.write(f"💰 {item.properties['discount_price']}")

                    # Feedback button
                    if st.button(f" Like {i}", key=f"{msg['content']}_{i}"):
                        store_feedback(item.properties["name"])
                        st.success("Saved preference ")