import requests

# LM Studio default API endpoint (adjust if needed)
LM_STUDIO_URL = "http://localhost:1234/v1/completions"
MODEL = "your-model-name"  # Replace with your LM Studio model name
PROMPT = "Tell me about Apple Inc. stock."

headers = {
    "Content-Type": "application/json"
}
payload = {
    "model": MODEL,
    "prompt": PROMPT,
    "max_tokens": 256,
    "temperature": 0.7
}

response = requests.post(LM_STUDIO_URL, headers=headers, json=payload)

if response.ok:
    print("Response:")
    print(response.json())
else:
    print(f"Error: {response.status_code}")
    print(response.text)
