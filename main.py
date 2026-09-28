from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "FitBuddy - AI Fitness Plan Generator is Running!"}

@app.post("/generate-plan")
def generate_plan(age: int, weight: int, goal: str):
    if goal == "weight loss":
        plan = "7-Day Plan: Daily 30min Cardio + Low carb diet"
    else:
        plan = "7-Day Plan: Weight Training + High Protein diet"
    return {"age": age, "weight": weight, "goal": goal, "plan": plan}
