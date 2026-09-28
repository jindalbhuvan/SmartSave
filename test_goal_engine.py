from database.goals import get_customer_goals
from src.goal_engine import generate_goal_summary


CUSTOMER_ID = "CUST0001"


goals = get_customer_goals(CUSTOMER_ID)


print("Customer:", CUSTOMER_ID)
print("=" * 60)


for goal in goals:

    summary = generate_goal_summary(goal)

    print("Goal:", summary["goal_name"])

    print(
        "Target Amount:",
        summary["target_amount"]
    )

    print(
        "Current Amount:",
        summary["current_amount"]
    )

    print(
        "Remaining Amount:",
        summary["remaining_amount"]
    )

    print(
        "Progress:",
        round(
            summary["progress_percentage"],
            2
        ),
        "%"
    )

    print(
        "Target Date:",
        summary["target_date"]
    )

    print(
        "Months Remaining:",
        summary["months_remaining"]
    )

    print(
        "Required Monthly Saving:",
        round(
            summary["required_monthly_saving"],
            2
        )
    )

    print(
        "Status:",
        summary["status"]
    )

    print("=" * 60)