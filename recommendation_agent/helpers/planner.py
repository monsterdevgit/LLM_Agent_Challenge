import json
from helpers.json_utils import extract_json

def planner(model, user_query, user_profile):

    prompt = f"""
User Query: {user_query}
User Profile: {user_profile}

Return JSON:
{{
 "search_query": "...",
 "category": "...",
 "reason": "..."
}}
"""

    res = model.generate_content(prompt).text
    return json.loads(extract_json(res))