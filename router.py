import openai
import json
import os
from prompts import SYSTEM_PROMPTS

# Function to classify user intent using LLM

def classify_intent(message: str) -> dict:
    classifier_prompt = """Your task is to classify the user's intent. Based on the user message below, choose one of the following labels: code, data, writing, career, unclear. Respond with a single JSON object containing two keys: 'intent' (the label you chose) and 'confidence' (a float from 0.0 to 1.0, representing your certainty). Do not provide any other text or explanation.

User message: {message}"""

    try:
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": classifier_prompt.format(message=message)}],
            max_tokens=100,
            temperature=0.0
        )
        result = response.choices[0].message.content.strip()
        try:
            parsed = json.loads(result)
            if "intent" in parsed and "confidence" in parsed:
                return parsed
            else:
                return {"intent": "unclear", "confidence": 0.0}
        except json.JSONDecodeError:
            return {"intent": "unclear", "confidence": 0.0}
    except Exception as e:
        print(f"Error in classification: {e}")
        return {"intent": "unclear", "confidence": 0.0}

# Function to route and respond based on intent

def route_and_respond(message: str, intent: dict) -> str:
    intent_label = intent["intent"]
    confidence = intent["confidence"]
    if intent_label == "unclear" or confidence < 0.7:
        return "I'm not sure what you're asking. Are you looking for help with coding, data analysis, writing, or career advice?"
    if intent_label not in SYSTEM_PROMPTS:
        return "Sorry, I don't have an expert for that intent."
    system_prompt = SYSTEM_PROMPTS[intent_label]
    try:
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error in response generation: {e}")
        return "Sorry, there was an error generating the response."

# Function to log requests

def log_request(intent: str, confidence: float, user_message: str, final_response: str):
    log_entry = {
        "intent": intent,
        "confidence": confidence,
        "user_message": user_message,
        "final_response": final_response
    }
    with open("route_log.jsonl", "a") as f:
        f.write(json.dumps(log_entry) + "\n")