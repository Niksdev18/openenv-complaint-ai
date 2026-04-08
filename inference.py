from dotenv import load_dotenv
load_dotenv()
import os
import requests
from openai import OpenAI
import json

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

BASE_URL = "http://127.0.0.1:8000"

def get_action(observation):
    prompt = f"""
Complaint: {observation['complaint']}

Choose next action:
classify / assign / prioritize

Return JSON:
{{"action_type":"...", "value":"..."}}
"""

    try:
        res = client.chat.completions.create(
            model=os.getenv("MODEL_NAME"),
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        return json.loads(res.choices[0].message.content)
    except:
        return {"action_type": "classify", "value": "infrastructure"}

def main():
    print("🚀 Starting AI agent...")

    r = requests.get(f"{BASE_URL}/reset")
    result = r.json()

    print("Complaint:", result["observation"]["complaint"])

    for i in range(5):
        action = get_action(result["observation"])
        print(f"Step {i+1} Action:", action)

        r = requests.post(f"{BASE_URL}/step", json=action)
        result = r.json()

        print("Reward:", result["reward"])

        if result["done"]:
            print("✅ Task completed")
            break

if __name__ == "__main__":
    main()