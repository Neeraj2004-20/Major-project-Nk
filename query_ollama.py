import requests

# Change these as needed
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "mistral"  # or your installed model name
PROMPT = "Tell me about Apple Inc. stock."

payload = {
    "model": MODEL,
    "prompt": PROMPT
}

response = requests.post(OLLAMA_URL, json=payload)

if response.ok:
    print("Response:")
    print(response.json())
else:
    print(f"Error: {response.status_code}")
    print(response.text)
