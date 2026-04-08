from app.models import Observation, Action, StepResult
from app.tasks import get_random_task
from app.grader import grade

class ComplaintEnv:
    def __init__(self):
        self.task = None
        self.actions = []
        self.done = False
        self.history = []

    def reset(self):
        self.task = get_random_task()
        self.actions = []
        self.done = False
        self.history = []

        return StepResult(
            observation=Observation(
                complaint=self.task["complaint"],
                status="started",
                history=[]
            ),
            reward=0.0,
            done=False
        )

    def step(self, action: Action):
        if self.done:
            return StepResult(
                observation=Observation(
                    complaint=self.task["complaint"],
                    status="done",
                    history=self.history
                ),
                reward=0.0,
                done=True
            )

        action_dict = action.dict()

        penalty = -0.2 if action_dict in self.actions else 0

        self.actions.append(action_dict)
        self.history.append(f"{action.action_type}:{action.value}")

        reward = 0.1 + penalty

        if len(self.actions) >= 3:
            self.done = True
            reward += grade(self.task, self.actions)

        return StepResult(
            observation=Observation(
                complaint=self.task["complaint"],
                status="in_progress",
                history=self.history,
                last_action=action.action_type
            ),
            reward=reward,
            done=self.done
        )

    def state(self):
        return {
            "task": self.task,
            "actions": self.actions,
            "history": self.history
        }