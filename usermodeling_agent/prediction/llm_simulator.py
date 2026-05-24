from helpers.prompt_builder import build_prompt
from helpers.generator import generate_review
from helpers.parser import extract_json


def simulate_user_response(client, user_features, history, product):

    prompt = build_prompt(user_features, history, product)

    raw = generate_review(client, prompt)

    return extract_json(raw)