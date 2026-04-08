from dotenv import load_dotenv
load_dotenv()

import os
import requests
import json

# ✅ Safe OpenAI import
try:
    from openai import OpenAI
except:
    OpenAI = None

# ✅ Safe API key handling
api_key = os.getenv("OPENAI_API_KEY")
client = None

if OpenAI and api_key:
    try:
        client = OpenAI(api_key=api_key)
    except:
        client = None

BASE_URL = "http://127.0.0.1:8000"

# ✅ Safe action generator
def get_action(observation):
    # 🔥 Fallback if no API key (VERY IMPORTANT)
    if client is None:
        return {"action_type": "classify", "value": "infrastructure"}

    prompt = f"""
Complaint: {observation['complaint']}

Choose next action:
classify / assign / prioritize

Return JSON:
{{"action_type":"...", "value":"..."}}
"""

    try:
        res = client.chat.completions.create(
            model=os.getenv("MODEL_NAME", "gpt-4o-mini"),
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        return json.loads(res.choices[0].message.content)
    except:
        # 🔥 fallback if API fails
        return {"action_type": "classify", "value": "infrastructure"}

# ✅ Safe main execution
def main():
    print("🚀 Starting AI agent...")

    try:
        r = requests.get(f"{BASE_URL}/reset", timeout=10)
        result = r.json()

        print("Complaint:", result["observation"]["complaint"])

        for i in range(5):
            action = get_action(result["observation"])
            print(f"Step {i+1} Action:", action)

            r = requests.post(f"{BASE_URL}/step", json=action, timeout=10)
            result = r.json()

            print("Reward:", result.get("reward", 0))

            if result.get("done"):
                print("✅ Task completed")
                break

    except Exception as e:
        # 🔥 IMPORTANT: never crash
        print("Error occurred:", e)

# ✅ Entry point
if __name__ == "__main__":
    main()