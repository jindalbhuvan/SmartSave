import pandas as pd

from database.queries import get_all_transactions


def load_mysql_transactions():
    df = get_all_transactions()

    df["transaction_date"] = pd.to_datetime(
        df["transaction_date"]
    )

    return df


def get_customer_transactions(df, customer_id):
    customer_df = df[
        df["customer_id"] == customer_id
    ].copy()

    return customer_df


def calculate_total_income(customer_df):
    income = customer_df[
        customer_df["transaction_type"] == "Income"
    ]["amount"].sum()

    return income


def calculate_total_expenses(customer_df):
    expenses = customer_df[
        customer_df["transaction_type"] == "Expense"
    ]["amount"].sum()

    return expenses


def calculate_savings(customer_df):
    income = calculate_total_income(customer_df)
    expenses = calculate_total_expenses(customer_df)

    return income - expenses


def calculate_savings_rate(customer_df):
    income = calculate_total_income(customer_df)
    savings = calculate_savings(customer_df)

    if income <= 0:
        return 0

    return (savings / income) * 100


def calculate_category_spending(customer_df):

    expenses = customer_df[
        customer_df["transaction_type"] == "Expense"
    ]

    category_spending = (
        expenses
        .groupby("category")["amount"]
        .sum()
        .sort_values(ascending=False)
    )

    return category_spending


def get_top_spending_category(customer_df):

    category_spending = calculate_category_spending(
        customer_df
    )

    if category_spending.empty:
        return None

    return category_spending.index[0]


def calculate_discretionary_spending(customer_df):

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


def calculate_essential_spending(customer_df):

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


def generate_spending_summary(customer_df):

    income = calculate_total_income(customer_df)
    expenses = calculate_total_expenses(customer_df)
    savings = calculate_savings(customer_df)
    savings_rate = calculate_savings_rate(customer_df)

    discretionary = calculate_discretionary_spending(
        customer_df
    )

    essential = calculate_essential_spending(
        customer_df
    )

    top_category = get_top_spending_category(
        customer_df
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