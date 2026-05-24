from helpers.user_utils import personality_to_style

def build_prompt(user_features, review_history, product):

    personality = f"""
Openness: {user_features['op']}
Conscientiousness: {user_features['co']}
Extraversion: {user_features['ex']}
Agreeableness: {user_features['ag']}
Neuroticism: {user_features['ne']}
Category: {user_features['categoria']}
"""

    style = personality_to_style(user_features)

    examples = ""
    for i, r in enumerate(review_history):
        examples += f"""
[Example {i+1}]
Review: {r['reviewText']}
Score: {r['overall']}
"""

    prompt = f"""
    You are simulating a user's product review behavior.

    User personality:
    {personality}

    Writing style:
    {style}

    Past behavior:
    {examples}

    New product:
    {product}

    Task:
    Predict rating (1–5) and generate review.

    Return ONLY VALID JSON.
    Do not include explanations.

    Format:
    {{
    "Review": "...",
    "Score": 1-5
    }}
"""

    return prompt