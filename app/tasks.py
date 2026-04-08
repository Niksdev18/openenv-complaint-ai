import random

TASKS = [
    {
        "complaint": "Street light not working in my area",
        "answer": {"category": "infrastructure", "department": "municipality", "priority": "medium"}
    },
    {
        "complaint": "Garbage not collected for 5 days",
        "answer": {"category": "sanitation", "department": "municipality", "priority": "high"}
    },
    {
        "complaint": "Water leakage and road damage",
        "answer": {"category": "infrastructure", "department": "PWD", "priority": "high"}
    },
    {
        "complaint": "पानी की समस्या है और सफाई नहीं हो रही",
        "answer": {"category": "sanitation", "department": "municipality", "priority": "high"}
    }
]

def get_random_task():
    return random.choice(TASKS)