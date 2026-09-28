from src.spending_analyzer import (
    load_transactions,
    get_customer_transactions,
    generate_spending_summary
)


# Load data
df = load_transactions()


# Select one customer
customer_df = get_customer_transactions(
    df,
    "CUST0001"
)


# Generate analysis
summary = generate_spending_summary(
    customer_df
)


print("\n===== SMARTSAVE SPENDING ANALYSIS =====\n")

print(
    "Total Income:",
    summary["total_income"]
)

print(
    "Total Expenses:",
    summary["total_expenses"]
)

print(
    "Savings:",
    summary["savings"]
)

print(
    "Savings Rate:",
    round(
        summary["savings_rate"],
        2
    ),
    "%"
)

print(
    "Essential Spending:",
    summary["essential_spending"]
)

print(
    "Discretionary Spending:",
    summary["discretionary_spending"]
)

print(
    "Top Spending Category:",
    summary["top_spending_category"]
)