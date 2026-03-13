from router import classify_intent, route_and_respond, log_request
from prompts import SYSTEM_PROMPTS

# Main function for CLI interaction

def main():
    message = input("Enter your message: ")
    if message.startswith("@"):
        parts = message.split(" ", 1)
        if len(parts) == 2:
            override_intent = parts[0][1:]  # remove @
            if override_intent in SYSTEM_PROMPTS or override_intent == "unclear":
                message = parts[1]
                intent = {"intent": override_intent, "confidence": 1.0}
            else:
                intent = classify_intent(message)  # original message
        else:
            intent = classify_intent(message)
    else:
        intent = classify_intent(message)
    response = route_and_respond(message, intent)
    log_request(intent["intent"], intent["confidence"], message, response)
    print(f"Intent: {intent['intent']} (confidence: {intent['confidence']})")
    print(f"Response: {response}")

# Test function with sample messages

def test():
    test_messages = [
        "how do i sort a list of objects in python?",
        "explain this sql query for me",
        "This paragraph sounds awkward, can you help me fix it?",
        "I'm preparing for a job interview, any tips?",
        "what's the average of these numbers: 12, 45, 23, 67, 34",
        "Help me make this better.",
        "I need to write a function that takes a user id and returns their profile, but also i need help with my resume.",
        "hey",
        "Can you write me a poem about clouds?",
        "Rewrite this sentence to be more professional.",
        "I'm not sure what to do with my career.",
        "what is a pivot table",
        "fxi thsi bug pls: for i in range(10) print(i)",
        "How do I structure a cover letter?",
        "My boss says my writing is too verbose."
    ]
    for msg in test_messages:
        print(f"Testing: {msg}")
        intent = classify_intent(msg)
        response = route_and_respond(msg, intent)
        log_request(intent["intent"], intent["confidence"], msg, response)
        print(f"Intent: {intent['intent']} (confidence: {intent['confidence']})")
        print(f"Response: {response}")
        print("-" * 50)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test()
    else:
        main()