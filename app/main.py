from fastapi import FastAPI
from app.env import ComplaintEnv
from app.models import Action

app = FastAPI()

env = ComplaintEnv()

@app.get("/")
def home():
    return {"message": "Complaint OpenEnv running"}


@app.post("/reset")
@app.get("/reset")
def reset():
    result = env.reset()
    return result.dict()


@app.post("/step")
def step(action: Action):
    result = env.step(action)
    return result.dict()


@app.get("/state")
def state():
    return env.state()