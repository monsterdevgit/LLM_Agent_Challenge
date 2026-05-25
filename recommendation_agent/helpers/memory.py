import json
from helpers.json_utils import extract_json

# Global user profile
user_profile = {
    "preferences": [],
    "taste": [],
    "budget": None,

    # NEW (behavioral persona)
    "features": [],          # camera, battery, gaming etc.
    "brands": [],            # Apple, Samsung, etc.
    "usage_style": None,     # casual, heavy, gaming, business
    "signals": []            # inferred behavior (e.g. "tech-savvy")
}

# Feedback storage
feedback = []

def store_feedback(product_name):
    feedback.append({"product": product_name})


def update_memory(model, user_input):

    global user_profile

    prompt = f"""
Extract user preferences from the message.

Return STRICT JSON ONLY:
{{
 "preferences": [],
 "taste": [],
 "budget": null,

 "features": [],
 "brands": [],
 "usage_style": null,
 "signals": []
}}

Guidelines:
- "features" → camera, battery, gaming, performance, durability
- "brands" → Apple, Samsung, etc.
- "usage_style" → casual, heavy, gaming, business
- "signals" → inferred behavior (e.g. "tech-savvy", "price-conscious")

Query: {user_input}
"""

    res = model.generate_content(prompt).text
    clean = extract_json(res)

    if clean:
        try:
            data = json.loads(clean)

            # EXISTING
            user_profile["preferences"] += data.get("preferences", [])
            user_profile["taste"] += data.get("taste", [])

            if data.get("budget"):
                user_profile["budget"] = data["budget"]

            # NEW ADDITIONS
            user_profile["features"] += data.get("features", [])
            user_profile["brands"] += data.get("brands", [])
            user_profile["signals"] += data.get("signals", [])

            if data.get("usage_style"):
                user_profile["usage_style"] = data["usage_style"]

        except Exception as e:
            print("Memory parsing failed")

    # EXISTING FEEDBACK LOGIC (kept)
    if feedback:
        liked_products = [f["product"] for f in feedback]
        user_profile["preferences"] += liked_products

    # NEW: deduplicate to keep memory clean
    for key in ["preferences", "taste", "features", "brands", "signals"]:
        user_profile[key] = list(set(user_profile[key]))

    return user_profile