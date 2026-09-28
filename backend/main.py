from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import date

from database.goals import (
    create_goal,
    get_customer_goals,
    add_contribution,
    get_goal_contributions
)

from src.goal_engine import (
    generate_goal_summary
)

from src.customer_health import (
    get_customer_health
)

from ml.goal_risk_model import (
    predict_goal_risk
)


app = FastAPI(
    title="SmartSave API",
    description="Goal-Based Personal Finance & Financial Wellness API",
    version="1.0.0"
)


# =========================================================
# REQUEST MODELS
# =========================================================

class GoalRequest(BaseModel):

    customer_id: str
    goal_name: str
    goal_category: str
    target_amount: float
    current_amount: float
    target_date: date


class ContributionRequest(BaseModel):

    goal_id: int
    contribution_date: date
    amount: float
    source: str


# =========================================================
# ROOT
# =========================================================

@app.get("/")
def root():

    return {
        "application": "SmartSave",
        "status": "running",
        "message": "SmartSave API is working"
    }


# =========================================================
# GET CUSTOMER GOALS
# =========================================================

@app.get("/goals/{customer_id}")
def get_goals(customer_id: str):

    try:

        goals = get_customer_goals(
            customer_id
        )

        results = []

        for goal in goals:

            results.append(
                generate_goal_summary(goal)
            )

        return {
            "customer_id": customer_id,
            "goals": results
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# CREATE GOAL
# =========================================================

@app.post("/goals")
def create_new_goal(
    request: GoalRequest
):

    try:

        goal_id = create_goal(

            customer_id=request.customer_id,

            goal_name=request.goal_name,

            goal_category=request.goal_category,

            target_amount=request.target_amount,

            current_amount=request.current_amount,

            target_date=request.target_date
        )

        return {
            "message": "Goal created successfully",
            "goal_id": goal_id
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# ADD CONTRIBUTION
# =========================================================

@app.post("/contributions")
def create_contribution(
    request: ContributionRequest
):

    try:

        contribution_id = add_contribution(

            goal_id=request.goal_id,

            contribution_date=
                request.contribution_date,

            amount=request.amount,

            source=request.source
        )

        return {
            "message":
                "Contribution added successfully",

            "contribution_id":
                contribution_id
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# GET CONTRIBUTION HISTORY
# =========================================================

@app.get("/contributions/{goal_id}")
def contribution_history(
    goal_id: int
):

    try:

        contributions = get_goal_contributions(
            goal_id
        )

        return {
            "goal_id": goal_id,
            "contributions": contributions
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# FINANCIAL HEALTH
# =========================================================

@app.get("/financial-health/{customer_id}")
def financial_health(
    customer_id: str
):

    try:

        result = get_customer_health(
            customer_id
        )

        return result

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# ML — GOAL ABANDONMENT RISK
# =========================================================

@app.get("/goal-risk/{customer_id}/{goal_id}")
def goal_risk(
    customer_id: str,
    goal_id: int
):

    try:

        # ---------------------------------------------
        # Get customer's goals
        # ---------------------------------------------

        goals = get_customer_goals(
            customer_id
        )

        selected_goal = None

        for goal in goals:

            if goal["goal_id"] == goal_id:

                selected_goal = goal

                break

        if selected_goal is None:

            raise HTTPException(
                status_code=404,
                detail="Goal not found"
            )

        # ---------------------------------------------
        # Goal summary
        # ---------------------------------------------

        summary = generate_goal_summary(
            selected_goal
        )

        # ---------------------------------------------
        # Contribution history
        # ---------------------------------------------

        contributions = get_goal_contributions(
            goal_id
        )

        contribution_frequency = len(
            contributions
        )

        if contributions:

            average_contribution = sum(
                float(c["amount"])
                for c in contributions
            ) / len(contributions)

        else:

            average_contribution = 0

        # ---------------------------------------------
        # Customer financial profile
        # ---------------------------------------------

        profile_result = get_customer_health(
            customer_id
        )

        profile = profile_result["profile"]

        income = float(
            profile["income"]
        )

        expenses = float(
            profile["expenses"]
        )

        # ---------------------------------------------
        # Savings rate
        # ---------------------------------------------

        if income > 0:

            savings_rate = (
                (income - expenses)
                / income
            )

        else:

            savings_rate = 0

        # ---------------------------------------------
        # ML prediction
        # ---------------------------------------------

        prediction = predict_goal_risk(

            income=income,

            expenses=expenses,

            savings_rate=savings_rate,

            target_amount=
                summary["target_amount"],

            goal_progress=
                summary["progress_percentage"],

            months_remaining=
                summary["months_remaining"],

            contribution_frequency=
                contribution_frequency,

            average_contribution=
                average_contribution
        )

        # ---------------------------------------------
        # API response
        # ---------------------------------------------

        return {

            "customer_id":
                customer_id,

            "goal_id":
                goal_id,

            "goal_name":
                summary["goal_name"],

            "risk_probability":
                prediction["risk_probability"],

            "risk_level":
                prediction["risk_level"],

            "contribution_count":
                contribution_frequency,

            "average_contribution":
                round(
                    average_contribution,
                    2
                )
        }

    except HTTPException:

        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# RUN SERVER
# =========================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "backend.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )