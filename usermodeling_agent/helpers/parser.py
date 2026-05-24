import json
import re

def extract_json(text):
    match = re.search(r"\{.*\}", text, re.DOTALL)

    if not match:
        return None

    raw_json = match.group(0)

    try:
        return json.loads(raw_json)

    except json.JSONDecodeError:

        # remove control characters
        cleaned = raw_json.replace("\n", " ").replace("\r", " ")

        # remove invalid quotes
        cleaned = re.sub(r'(?<!\\)"', '"', cleaned)

        try:
            return json.loads(cleaned)

        except:
            print("[WARN] Could not parse JSON:")
            print(raw_json)
            return None