from openai import OpenAI
import matplotlib.pyplot as plt

print("Starting Market Sentiment Pipeline...")

client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio"
)

MODEL_NAME = "openhermes-2.5-mistral-7b"  # Change if needed

news_headlines = [
    "TCS reports strong quarterly profit growth.",
    "Reliance shares fall after weak earnings report.",
    "Infosys announces major global expansion plan."
]

def analyze_sentiment(news):
    print(f"\nSending to LLM: {news}")

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a financial sentiment analysis expert."},
            {"role": "user", "content": f"Classify as Positive, Neutral, or Negative: {news}"}
        ],
        temperature=0.1
    )

    result = response.choices[0].message.content.strip()
    print("Received:", result)
    return result

sentiment_results = []

for headline in news_headlines:
    sentiment = analyze_sentiment(headline)
    sentiment_results.append(sentiment)

print("\nAll Results:", sentiment_results)

positive = sentiment_results.count("Positive")
neutral = sentiment_results.count("Neutral")
negative = sentiment_results.count("Negative")

print("\nCounts:")
print("Positive:", positive)
print("Neutral:", neutral)
print("Negative:", negative)

labels = ["Positive", "Neutral", "Negative"]
values = [positive, neutral, negative]

plt.figure()
plt.bar(labels, values)
plt.title("LLM-Based Market Sentiment Distribution")
plt.xlabel("Sentiment")
plt.ylabel("Count")
plt.show()