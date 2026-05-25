import json
import re
from helpers.memory import feedback

def rerank(model, query, items):

    if not items:
        return []

    names = [i.properties["name"] for i in items]

    prompt = f"""
Rank products by relevance.

Query: {query}

Products:
{names}

Return JSON list sorted best first.
"""

    res = model.generate_content(prompt).text

    match = re.search(r'\[.*\]', res, re.DOTALL)

    # fallback if Gemini fails
    if not match:
        ranked_items = items
    else:
        try:
            ranked_names = json.loads(match.group(0))

            ranked_items = []

            for name in ranked_names:
                for item in items:
                    if item.properties["name"] == name:
                        ranked_items.append(item)

        except Exception:
            ranked_items = items

    # boost items based on feedback
    if feedback:
        liked_products = [f["product"] for f in feedback]

        boosted = []

        # Move liked items to top
        for item in ranked_items:
            if item.properties["name"] in liked_products:
                boosted.insert(0, item)
            else:
                boosted.append(item)

        return boosted

    return ranked_items