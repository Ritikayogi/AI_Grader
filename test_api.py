import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

try:
    r = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Say hello in one line"}]
    )
    print("✅ API connected successfully!")
    print("GPT Response:", r.choices[0].message.content)
except Exception as e:
    print("❌ API Error:", e)

