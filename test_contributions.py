from datetime import date

from database.goals import (
    add_contribution,
    get_goal_contributions,
    get_customer_goals
)


# ---------------------------------------------------------
# SETTINGS
# ---------------------------------------------------------

CUSTOMER_ID = "CUST0001"
GOAL_ID = 4


# ---------------------------------------------------------
# 1. ADD A CONTRIBUTION
# ---------------------------------------------------------

print("Adding contribution...")

contribution_id = add_contribution(
    goal_id=GOAL_ID,
    contribution_date=date.today(),
    amount=5000,
    source="Monthly Savings"
)

print("Contribution created successfully!")
print("Contribution ID:", contribution_id)


# ---------------------------------------------------------
# 2. GET CONTRIBUTION HISTORY
# ---------------------------------------------------------

print("\nContribution History:")
print("-" * 50)

contributions = get_goal_contributions(GOAL_ID)

for contribution in contributions:
    print(
        "Contribution ID:",
        contribution["contribution_id"]
    )

    print(
        "Date:",
        contribution["contribution_date"]
    )

    print(
        "Amount:",
        contribution["amount"]
    )

    print(
        "Source:",
        contribution["source"]
    )

    print("-" * 50)


# ---------------------------------------------------------
# 3. GET CUSTOMER GOALS
# ---------------------------------------------------------

print("\nUpdated Goals:")
print("-" * 50)

goals = get_customer_goals(CUSTOMER_ID)

for goal in goals:

    print(
        "Goal:",
        goal["goal_name"]
    )

    print(
        "Target Amount:",
        goal["target_amount"]
    )

    print(
        "Current Amount:",
        goal["current_amount"]
    )

    print(
        "Target Date:",
        goal["target_date"]
    )

    print(
        "Status:",
        goal["status"]
    )

    print("-" * 50)