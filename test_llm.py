from openai import OpenAI

print("Connecting to LM Studio...")

client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio"
)

print("Sending request...")

response = client.chat.completions.create(
    model="openhermes-2.5-mistral-7b",  # Replace if different
    messages=[
        {"role": "system", "content": "You are a financial sentiment analyst."},
        {"role": "user", "content": "Classify sentiment as Positive, Neutral, or Negative: TCS reports strong quarterly profit growth."}
    ],
    temperature=0.2
)

print("Response received:")
print(response.choices[0].message.content)