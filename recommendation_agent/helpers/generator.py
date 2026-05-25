def generate_response(model, user_input, persona, items):

    prompt = f"""
You are an intelligent recommendation assistant.

You MUST:
- Use the user's persona + current request
- Recommend relevant items
- Be conversational (chat-like)
- Explain WHY each recommendation fits the user
- Include suggestions beyond products if relevant (movies, food, drinks)

---------------------
USER PERSONA:
{persona}

CURRENT USER MESSAGE:
"{user_input}"

AVAILABLE PRODUCTS:
{[item.properties for item in items]}

---------------------

Respond in this format:

Start with a short conversational reply.

Then give 3–5 personalized recommendations:

1. Name
   - Why it matches the user
   - Key detail (price, rating, category)

End with a smart follow-up suggestion.
"""

    response = model.generate_content(prompt)

    return response.text