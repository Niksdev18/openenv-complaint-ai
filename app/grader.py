from app.utils import fuzzy_match

def grade(task, actions):
    score = 0.0
    ans = task["answer"]

    for act in actions:
        if act["action_type"] == "classify":
            if fuzzy_match(act["value"], ans["category"]):
                score += 0.4

        elif act["action_type"] == "assign":
            if fuzzy_match(act["value"], ans["department"]):
                score += 0.3

        elif act["action_type"] == "prioritize":
            if fuzzy_match(act["value"], ans["priority"]):
                score += 0.3

    return min(score, 1.0)