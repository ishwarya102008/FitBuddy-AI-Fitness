from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from .schemas import UserInput
from .database import (
    save_user,
    save_plan,
    get_user,
    update_plan,
    get_all_users
)

from .gemini_generator import generate_workout_gemini
from .gemini_flash_generator import generate_nutrition_tip_with_flash
from .updated_plan import update_workout_plan


router = APIRouter()

templates = Jinja2Templates(
    directory="templates"
)


@router.get("/", response_class=HTMLResponse)
def home(request: Request):

    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


@router.post("/generate-workout", response_class=HTMLResponse)
def generate_workout(
    request: Request,
    user_id: str = Form(...),
    username: str = Form(...),
    age: int = Form(...),
    weight: str = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...)
):

    user = UserInput(
        user_id=user_id,
        username=username,
        age=age,
        weight=weight,
        goal=goal,
        intensity=intensity
    )

    workout_plan = generate_workout_gemini(
        user.username,
        user.age,
        user.weight,
        user.goal,
        user.intensity
    )

    nutrition_tip = generate_nutrition_tip_with_flash(
        user.goal
    )

    save_user(
        user.user_id,
        user.username,
        user.age,
        user.weight,
        user.goal,
        user.intensity
    )

    save_plan(
        user.user_id,
        workout_plan
    )

    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "username": user.username,
            "user_id": user.user_id,
            "age": user.age,
            "weight": user.weight,
            "goal": user.goal,
            "intensity": user.intensity,
            "workout_plan": workout_plan,
            "nutrition_tip": nutrition_tip
        }
    )


@router.post("/submit-feedback", response_class=HTMLResponse)
def submit_feedback(
    request: Request,
    user_id: str = Form(...),
    feedback: str = Form(...)
):

    user = get_user(user_id)

    if not user:
        return HTMLResponse(
            "User not found",
            status_code=404
        )

    updated = update_workout_plan(
        user.original_plan,
        feedback
    )

    update_plan(
        user_id,
        updated
    )

    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "username": user.username,
            "user_id": user.user_id,
            "age": user.age,
            "weight": user.weight,
            "goal": user.goal,
            "intensity": user.intensity,
            "workout_plan": updated,
            "nutrition_tip": "Your workout plan has been updated based on your feedback."
        }
    )


@router.get("/view-all-users", response_class=HTMLResponse)
def view_all_users(request: Request):

    users = get_all_users()

    return templates.TemplateResponse(
        "all_users.html",
        {
            "request": request,
            "users": users
        }
  )
