from src.customer_financial_profile import (
    get_customer_financial_profile
)

from src.financial_health import (
    calculate_financial_health,
    generate_recommendations
)

from database.goals import get_customer_goals

from src.goal_engine import (
    generate_goal_summary
)


def get_customer_health(customer_id):

    profile = get_customer_financial_profile(
        customer_id
    )

    income = profile["income"]
    expenses = profile["expenses"]
    savings = profile["savings"]

    # --------------------------------
    # Goal information
    # --------------------------------

    goals = get_customer_goals(
        customer_id
    )

    if goals:

        progress_values = []

        for goal in goals:

            summary = generate_goal_summary(
                goal
            )

            progress_values.append(
                summary["progress_percentage"]
            )

        goal_progress = sum(
            progress_values
        ) / len(progress_values)

    else:

        goal_progress = 0

    # --------------------------------
    # Temporary assumptions
    # --------------------------------
    # These will later come from
    # dedicated financial/debt data.

    monthly_debt = 0

    emergency_fund = 0

    monthly_essential_expenses = expenses * 0.60

    # --------------------------------
    # Financial Health
    # --------------------------------

    health = calculate_financial_health(

        monthly_income=income,

        monthly_expenses=expenses,

        monthly_savings=savings,

        monthly_debt=monthly_debt,

        emergency_fund=emergency_fund,

        monthly_essential_expenses=
            monthly_essential_expenses,

        goal_progress=goal_progress
    )

    recommendations = generate_recommendations(
        health
    )

    return {
        "profile": profile,
        "health": health,
        "recommendations": recommendations
    }