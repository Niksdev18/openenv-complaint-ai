from pydantic import BaseModel
from typing import Optional, List, Dict

class Observation(BaseModel):
    complaint: str
    status: str
    history: List[str] = []
    last_action: Optional[str] = None

class Action(BaseModel):
    action_type: str
    value: str

class StepResult(BaseModel):
    observation: Observation
    reward: float
    done: bool
    info: Dict = {}