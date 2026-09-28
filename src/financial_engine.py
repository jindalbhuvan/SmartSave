from datetime import date


def calculate_financial_plan(
    income,
    rent,
    food,
    transport,
    utilities,
    shopping,
    entertainment,
    insurance,
    subscriptions,
    other_expenses,
    monthly_emi,
    current_savings,
    emergency_fund,
    goal_type,
    target_amount,
    goal_saved,
    target_date
):

    # ========================================================
    # TOTAL EXPENSES
    # ========================================================

    total_expenses = (
        rent
        + food
        + transport
        + utilities
        + shopping
        + entertainment
        + insurance
        + subscriptions
        + other_expenses
        + monthly_emi
    )


    # ========================================================
    # MONTHLY SURPLUS
    # ========================================================

    monthly_surplus = (
        income - total_expenses
    )


    # ========================================================
    # SAVINGS RATE
    # ========================================================

    if income > 0:

        savings_rate = (
            monthly_surplus / income
        ) * 100

    else:

        savings_rate = 0


    # ========================================================
    # EXPENSE RATIO
    # ========================================================

    if income > 0:

        expense_ratio = (
            total_expenses / income
        ) * 100

    else:

        expense_ratio = 100


    # ========================================================
    # DEBT-TO-INCOME RATIO
    # ========================================================

    if income > 0:

        debt_to_income = (
            monthly_emi / income
        ) * 100

    else:

        debt_to_income = 100


    # ========================================================
    # ESSENTIAL EXPENSES
    # ========================================================

    essential_expenses = (
        rent
        + food
        + transport
        + utilities
        + insurance
        + other_expenses
    )


    if income > 0:

        essential_expense_ratio = (
            essential_expenses / income
        ) * 100

    else:

        essential_expense_ratio = 0


    # ========================================================
    # DISCRETIONARY EXPENSES
    # ========================================================

    discretionary_expenses = (
        shopping
        + entertainment
        + subscriptions
    )


    if income > 0:

        discretionary_expense_ratio = (
            discretionary_expenses / income
        ) * 100

    else:

        discretionary_expense_ratio = 0


    # ========================================================
    # EMERGENCY FUND COVERAGE
    # ========================================================

    monthly_living_expenses = (
        total_expenses - monthly_emi
    )

    if monthly_living_expenses > 0:

        emergency_fund_months = (
            emergency_fund
            / monthly_living_expenses
        )

    else:

        emergency_fund_months = 0


    # ========================================================
    # GOAL CALCULATION
    # ========================================================

    remaining_goal = max(
        target_amount - goal_saved,
        0
    )


    today = date.today()

    months_remaining = (
        (target_date.year - today.year) * 12
        + target_date.month
        - today.month
    )

    months_remaining = max(
        months_remaining,
        1
    )


    required_monthly_saving = (
        remaining_goal
        / months_remaining
    )


    # ========================================================
    # GOAL FEASIBILITY
    # ========================================================

    goal_achievable = (
        monthly_surplus > 0
        and monthly_surplus >= required_monthly_saving
    )


    # ========================================================
    # FINANCIAL HEALTH SCORE
    # ========================================================

    # Savings component: maximum 35 points
    savings_component = min(
        max(savings_rate, 0) / 25 * 35,
        35
    )


    # Debt component: maximum 25 points
    if debt_to_income <= 10:

        debt_component = 25

    elif debt_to_income <= 20:

        debt_component = 20

    elif debt_to_income <= 30:

        debt_component = 15

    elif debt_to_income <= 40:

        debt_component = 8

    else:

        debt_component = 0


    # Emergency fund: maximum 25 points
    emergency_component = min(
        emergency_fund_months / 6 * 25,
        25
    )


    # Expense management: maximum 15 points
    if expense_ratio <= 60:

        expense_component = 15

    elif expense_ratio <= 70:

        expense_component = 12

    elif expense_ratio <= 80:

        expense_component = 9

    elif expense_ratio <= 90:

        expense_component = 5

    else:

        expense_component = 0


    health_score = round(
        savings_component
        + debt_component
        + emergency_component
        + expense_component
    )

    health_score = min(
        max(health_score, 0),
        100
    )


    # ========================================================
    # RETURN RESULTS
    # ========================================================

    return {

        "income": income,

        "total_expenses": total_expenses,

        "monthly_surplus": monthly_surplus,

        "savings_rate": savings_rate,

        "expense_ratio": expense_ratio,

        "debt_to_income": debt_to_income,

        "essential_expenses": essential_expenses,

        "essential_expense_ratio": essential_expense_ratio,

        "discretionary_expenses": discretionary_expenses,

        "discretionary_expense_ratio":
            discretionary_expense_ratio,

        "current_savings": current_savings,

        "emergency_fund": emergency_fund,

        "emergency_fund_months":
            emergency_fund_months,

        "monthly_emi": monthly_emi,

        "goal_type": goal_type,

        "target_amount": target_amount,

        "goal_saved": goal_saved,

        "remaining_goal": remaining_goal,

        "target_date": target_date,

        "months_remaining": months_remaining,

        "required_monthly_saving":
            required_monthly_saving,

        "goal_achievable":
            goal_achievable,

        "health_score":
            health_score
    }