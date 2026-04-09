from dotenv import load_dotenv
load_dotenv()

import os
import requests
import json

# Safe OpenAI import
try:
    from openai import OpenAI
except:
    OpenAI = None

# Safe API key handling
api_key = os.getenv("OPENAI_API_KEY")
client = None

if OpenAI and api_key:
    try:
        client = OpenAI(api_key=api_key)
    except:
        client = None

BASE_URL = "http://127.0.0.1:8000"

# Safe action generator
def get_action(observation):
    # Fallback if no API key
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
        return {"action_type": "classify", "value": "infrastructure"}


# 🔥 CRITICAL: Structured output main
def main():
    try:
        r = requests.get(f"{BASE_URL}/reset", timeout=10)
        result = r.json()

        task_name = "complaint"

        # START block
        print(f"[START] task={task_name}", flush=True)

        steps = 0
        total_reward = 0.0

        for i in range(5):
            action = get_action(result["observation"])

            r = requests.post(f"{BASE_URL}/step", json=action, timeout=10)
            result = r.json()

            reward = float(result.get("reward", 0))
            total_reward += reward
            steps += 1

            # STEP block
            print(f"[STEP] step={steps} reward={reward}", flush=True)

            if result.get("done"):
                break

        # END block
        print(f"[END] task={task_name} score={total_reward} steps={steps}", flush=True)

    except Exception:
        # Even on error, print valid structure
        print("[START] task=error", flush=True)
        print("[END] task=error score=0 steps=0", flush=True)


if __name__ == "__main__":
    main()