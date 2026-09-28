from datetime import date


def calculate_goal_progress(
    target_amount,
    current_amount
):
    if target_amount <= 0:
        return 0

    progress = (
        current_amount / target_amount
    ) * 100

    # Don't allow progress above 100%
    progress = min(progress, 100)

    return progress


def calculate_remaining_amount(
    target_amount,
    current_amount
):
    remaining = target_amount - current_amount

    # If user has already reached the target
    # remaining amount should not become negative.
    return max(remaining, 0)


def calculate_months_remaining(target_date):
    today = date.today()

    if target_date <= today:
        return 0

    months = (
        (target_date.year - today.year) * 12
        + target_date.month
        - today.month
    )

    # If there are remaining days in the target month,
    # count that month as well.
    if target_date.day >= today.day:
        months += 1

    return max(months, 1)


def calculate_required_monthly_saving(
    target_amount,
    current_amount,
    target_date
):
    remaining_amount = calculate_remaining_amount(
        target_amount,
        current_amount
    )

    months_remaining = calculate_months_remaining(
        target_date
    )

    if remaining_amount <= 0:
        return 0

    if months_remaining <= 0:
        return remaining_amount

    monthly_saving = (
        remaining_amount / months_remaining
    )

    return monthly_saving


def calculate_goal_status(
    target_amount,
    current_amount,
    target_date
):
    if current_amount >= target_amount:
        return "Completed"

    if target_date <= date.today():
        return "Overdue"

    return "Active"


def generate_goal_summary(goal):
    target_amount = float(
        goal["target_amount"]
    )

    current_amount = float(
        goal["current_amount"]
    )

    target_date = goal["target_date"]

    progress = calculate_goal_progress(
        target_amount,
        current_amount
    )

    remaining_amount = calculate_remaining_amount(
        target_amount,
        current_amount
    )

    months_remaining = calculate_months_remaining(
        target_date
    )

    monthly_saving = calculate_required_monthly_saving(
        target_amount,
        current_amount,
        target_date
    )

    status = calculate_goal_status(
        target_amount,
        current_amount,
        target_date
    )

    return {
        "goal_id": goal["goal_id"],
        "goal_name": goal["goal_name"],
        "target_amount": target_amount,
        "current_amount": current_amount,
        "remaining_amount": remaining_amount,
        "progress_percentage": progress,
        "target_date": target_date,
        "months_remaining": months_remaining,
        "required_monthly_saving": monthly_saving,
        "status": status
    }