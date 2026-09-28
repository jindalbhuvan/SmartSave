import pandas as pd


# ============================================================
# LOAD TRANSACTIONS
# ============================================================

def load_transactions(file_path="data/transactions.csv"):
    """
    Load transaction data from CSV.
    """

    df = pd.read_csv(file_path)

    df["transaction_date"] = pd.to_datetime(
        df["transaction_date"]
    )

    return df


# ============================================================
# USER TRANSACTIONS
# ============================================================

def get_customer_transactions(
    df,
    customer_id
):
    """
    Return all transactions for a particular customer.
    """

    customer_df = df[
        df["customer_id"] == customer_id
    ].copy()

    return customer_df


# ============================================================
# TOTAL INCOME
# ============================================================

def calculate_total_income(
    customer_df
):
    """
    Calculate total income for a customer.
    """

    income = customer_df[
        customer_df["transaction_type"] == "Income"
    ]["amount"].sum()

    return income


# ============================================================
# TOTAL EXPENSES
# ============================================================

def calculate_total_expenses(
    customer_df
):
    """
    Calculate total expenses for a customer.
    """

    expenses = customer_df[
        customer_df["transaction_type"] == "Expense"
    ]["amount"].sum()

    return expenses


# ============================================================
# SAVINGS
# ============================================================

def calculate_savings(
    customer_df
):
    """
    Calculate income minus expenses.
    """

    income = calculate_total_income(
        customer_df
    )

    expenses = calculate_total_expenses(
        customer_df
    )

    savings = income - expenses

    return savings


# ============================================================
# SAVINGS RATE
# ============================================================

def calculate_savings_rate(
    customer_df
):
    """
    Calculate savings rate as a percentage.
    """

    income = calculate_total_income(
        customer_df
    )

    savings = calculate_savings(
        customer_df
    )

    if income <= 0:
        return 0

    savings_rate = (
        savings / income
    ) * 100

    return savings_rate


# ============================================================
# CATEGORY SPENDING
# ============================================================

def calculate_category_spending(
    customer_df
):
    """
    Calculate total spending by category.
    """

    expenses = customer_df[
        customer_df["transaction_type"] == "Expense"
    ]

    category_spending = (
        expenses
        .groupby("category")["amount"]
        .sum()
        .sort_values(
            ascending=False
        )
    )

    return category_spending


# ============================================================
# TOP SPENDING CATEGORY
# ============================================================

def get_top_spending_category(
    customer_df
):
    """
    Identify the customer's highest
    spending category.
    """

    category_spending = (
        calculate_category_spending(
            customer_df
        )
    )

    if category_spending.empty:
        return None

    return category_spending.index[0]


# ============================================================
# DISCRETIONARY SPENDING
# ============================================================

def calculate_discretionary_spending(
    customer_df
):
    """
    Calculate spending in categories that
    may be more adjustable.

    This is a project-level classification,
    not a financial rule.
    """

    discretionary_categories = [
        "Shopping",
        "Entertainment",
        "Subscriptions",
        "Food"
    ]

    expenses = customer_df[
        customer_df["transaction_type"] == "Expense"
    ]

    discretionary = expenses[
        expenses["category"].isin(
            discretionary_categories
        )
    ]["amount"].sum()

    return discretionary


# ============================================================
# ESSENTIAL SPENDING
# ============================================================

def calculate_essential_spending(
    customer_df
):
    """
    Calculate spending in essential categories.
    """

    essential_categories = [
        "Rent",
        "Utilities",
        "Transport",
        "Healthcare",
        "Insurance",
        "Education"
    ]

    expenses = customer_df[
        customer_df["transaction_type"] == "Expense"
    ]

    essential = expenses[
        expenses["category"].isin(
            essential_categories
        )
    ]["amount"].sum()

    return essential


# ============================================================
# SPENDING SUMMARY
# ============================================================

def generate_spending_summary(
    customer_df
):
    """
    Generate a complete spending summary
    for a customer.
    """

    income = calculate_total_income(
        customer_df
    )

    expenses = calculate_total_expenses(
        customer_df
    )

    savings = calculate_savings(
        customer_df
    )

    savings_rate = calculate_savings_rate(
        customer_df
    )

    discretionary = (
        calculate_discretionary_spending(
            customer_df
        )
    )

    essential = (
        calculate_essential_spending(
            customer_df
        )
    )

    top_category = (
        get_top_spending_category(
            customer_df
        )
    )

    return {
        "total_income": income,
        "total_expenses": expenses,
        "savings": savings,
        "savings_rate": savings_rate,
        "essential_spending": essential,
        "discretionary_spending": discretionary,
        "top_spending_category": top_category
    }