# LLM-Powered Prompt Router

This is a Python service that intelligently routes user requests to specialized AI personas based on intent classification.

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Set your OpenAI API key:
   ```
   export OPENAI_API_KEY=your_api_key_here
   ```

## Usage

Run the CLI:
```
python main.py
```
Enter your message, and it will classify the intent and provide a response.

For testing with sample messages:
```
python main.py test
```

## Manual Override

Prefix your message with @intent to bypass classification, e.g., "@code how do I sort a list in Python?"

## Features

- Intent classification using LLM
- Routing to expert personas: code, data, writing, career
- Confidence threshold (0.7)
- Logging to route_log.jsonl
- Handles malformed JSON responses gracefully
- Docker containerization support

## Docker Usage

Build and run with Docker:
```
docker build -t llm-router .
docker run -e OPENAI_API_KEY=your_key llm-router
```