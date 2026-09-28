import joblib
import numpy as np


MODEL_PATH = "models/goal_abandonment_model.pkl"


model = joblib.load(MODEL_PATH)


def predict_goal_risk(
    income,
    expenses,
    savings_rate,
    target_amount,
    goal_progress,
    months_remaining,
    contribution_frequency,
    average_contribution
):

    features = np.array([[
        income,
        expenses,
        savings_rate,
        target_amount,
        goal_progress,
        months_remaining,
        contribution_frequency,
        average_contribution
    ]])

    probability = model.predict_proba(
        features
    )[0][1]

    probability_percentage = probability * 100

    if probability_percentage >= 70:
        risk_level = "High"

    elif probability_percentage >= 40:
        risk_level = "Medium"

    else:
        risk_level = "Low"

    return {
        "risk_probability": round(
            probability_percentage,
            2
        ),
        "risk_level": risk_level
    }