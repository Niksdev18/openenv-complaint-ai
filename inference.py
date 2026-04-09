from dotenv import load_dotenv
load_dotenv()

import os
import requests
import json

# Safe OpenAI import
client = None
try:
    from openai import OpenAI
    api_key = os.getenv("OPENAI_API_KEY")

    if api_key:
        client = OpenAI(api_key=api_key)
except:
    client = None

BASE_URL = "http://127.0.0.1:8000"


def get_action(observation):
    # Always safe fallback
    if client is None:
        return {"action_type": "classify", "value": "infrastructure"}

    try:
        prompt = f"""
Complaint: {observation.get('complaint', '')}

Choose next action:
classify / assign / prioritize

Return JSON:
{{"action_type":"...", "value":"..."}}
"""

        res = client.chat.completions.create(
            model=os.getenv("MODEL_NAME", "gpt-4o-mini"),
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        return json.loads(res.choices[0].message.content)

    except:
        return {"action_type": "classify", "value": "infrastructure"}


def main():
    task_name = "complaint"

    try:
        # Try reset
        r = requests.get(f"{BASE_URL}/reset", timeout=10)
        result = r.json()
        observation = result.get("observation", {})

    except:
        # Even if API fails → still print valid structure
        print(f"[START] task={task_name}", flush=True)
        print(f"[END] task={task_name} score=0 steps=0", flush=True)
        return

    # START
    print(f"[START] task={task_name}", flush=True)

    steps = 0
    total_reward = 0.0

    try:
        for i in range(5):
            action = get_action(observation)

            r = requests.post(f"{BASE_URL}/step", json=action, timeout=10)
            result = r.json()

            reward = float(result.get("reward", 0))
            observation = result.get("observation", {})

            total_reward += reward
            steps += 1

            print(f"[STEP] step={steps} reward={reward}", flush=True)

            if result.get("done"):
                break

    except:
        pass  # never crash

    # END (always printed)
    print(f"[END] task={task_name} score={total_reward} steps={steps}", flush=True)


if __name__ == "__main__":
    main()