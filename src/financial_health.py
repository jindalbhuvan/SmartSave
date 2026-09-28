def calculate_financial_health(
    monthly_income,
    monthly_expenses,
    monthly_savings,
    monthly_debt,
    emergency_fund,
    monthly_essential_expenses,
    goal_progress=0
):
    # -----------------------------
    # 1. Savings Rate
    # -----------------------------
    if monthly_income > 0:
        savings_rate = (
            monthly_savings / monthly_income
        ) * 100
    else:
        savings_rate = 0

    # -----------------------------
    # 2. Expense Ratio
    # -----------------------------
    if monthly_income > 0:
        expense_ratio = (
            monthly_expenses / monthly_income
        ) * 100
    else:
        expense_ratio = 100

    # -----------------------------
    # 3. Debt-to-Income Ratio
    # -----------------------------
    if monthly_income > 0:
        debt_to_income = (
            monthly_debt / monthly_income
        ) * 100
    else:
        debt_to_income = 100

    # -----------------------------
    # 4. Emergency Fund Coverage
    # -----------------------------
    if monthly_essential_expenses > 0:
        emergency_months = (
            emergency_fund /
            monthly_essential_expenses
        )
    else:
        emergency_months = 0

    # -----------------------------
    # 5. Individual Scores
    # -----------------------------

    # Savings score
    if savings_rate >= 30:
        savings_score = 25
    elif savings_rate >= 20:
        savings_score = 20
    elif savings_rate >= 10:
        savings_score = 15
    elif savings_rate > 0:
        savings_score = 8
    else:
        savings_score = 0

    # Expense score
    if expense_ratio <= 50:
        expense_score = 20
    elif expense_ratio <= 65:
        expense_score = 16
    elif expense_ratio <= 75:
        expense_score = 12
    elif expense_ratio <= 85:
        expense_score = 6
    else:
        expense_score = 0

    # Debt score
    if debt_to_income <= 20:
        debt_score = 20
    elif debt_to_income <= 35:
        debt_score = 15
    elif debt_to_income <= 50:
        debt_score = 8
    else:
        debt_score = 0

    # Emergency fund score
    if emergency_months >= 6:
        emergency_score = 20
    elif emergency_months >= 3:
        emergency_score = 15
    elif emergency_months >= 1:
        emergency_score = 8
    else:
        emergency_score = 0

    # Goal progress score
    if goal_progress >= 75:
        goal_score = 15
    elif goal_progress >= 50:
        goal_score = 12
    elif goal_progress >= 25:
        goal_score = 8
    elif goal_progress > 0:
        goal_score = 4
    else:
        goal_score = 0

    # -----------------------------
    # Final Score
    # -----------------------------
    score = (
        savings_score
        + expense_score
        + debt_score
        + emergency_score
        + goal_score
    )

    # -----------------------------
    # Financial Segment
    # -----------------------------
    if score >= 80:
        segment = "Goal-Oriented Saver"

    elif score >= 60:
        segment = "Potential Saver"

    elif score >= 40:
        segment = "Irregular Saver"

    else:
        segment = "Financially Constrained"

    return {
        "financial_health_score": round(score, 2),
        "savings_rate": round(savings_rate, 2),
        "expense_ratio": round(expense_ratio, 2),
        "debt_to_income": round(debt_to_income, 2),
        "emergency_fund_months": round(
            emergency_months,
            2
        ),
        "goal_progress": round(
            goal_progress,
            2
        ),
        "segment": segment
    }


def generate_recommendations(health):
    recommendations = []

    if health["savings_rate"] < 20:
        recommendations.append(
            "Try increasing your monthly savings "
            "towards at least 20% of income."
        )

    if health["expense_ratio"] > 70:
        recommendations.append(
            "Your expenses are relatively high "
            "compared with your income. Review "
            "discretionary spending."
        )

    if health["debt_to_income"] > 35:
        recommendations.append(
            "Your debt-to-income ratio is elevated. "
            "Consider prioritizing debt repayment."
        )

    if health["emergency_fund_months"] < 3:
        recommendations.append(
            "Build an emergency fund covering at "
            "least 3 months of essential expenses."
        )

    if health["goal_progress"] < 25:
        recommendations.append(
            "Your goal progress is still low. "
            "Consider setting up a consistent "
            "monthly contribution."
        )

    if not recommendations:
        recommendations.append(
            "Your financial indicators are relatively "
            "healthy. Continue maintaining your "
            "current savings discipline."
        )

    return recommendations