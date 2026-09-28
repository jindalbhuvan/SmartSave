import pandas as pd
import numpy as np

# ============================================================
# CONFIGURATION
# ============================================================

NUM_USERS = 500
MONTHS = 6

np.random.seed(42)


# ============================================================
# EXPENSE CATEGORIES
# ============================================================

expense_categories = [
    "Food",
    "Transport",
    "Shopping",
    "Entertainment",
    "Utilities",
    "Healthcare",
    "Insurance",
    "Education",
    "Rent",
    "Subscriptions",
    "Other"
]


descriptions = {
    "Food": [
        "Swiggy",
        "Zomato",
        "Restaurant",
        "Groceries"
    ],

    "Transport": [
        "Uber",
        "Ola",
        "Fuel",
        "Metro"
    ],

    "Shopping": [
        "Amazon",
        "Flipkart",
        "Clothing",
        "Electronics"
    ],

    "Entertainment": [
        "Movie",
        "Gaming",
        "Concert",
        "Streaming"
    ],

    "Utilities": [
        "Electricity",
        "Water Bill",
        "Internet",
        "Mobile Bill"
    ],

    "Healthcare": [
        "Pharmacy",
        "Doctor",
        "Medical Test"
    ],

    "Insurance": [
        "Health Insurance",
        "Life Insurance"
    ],

    "Education": [
        "Course",
        "Books",
        "Training"
    ],

    "Rent": [
        "Monthly Rent"
    ],

    "Subscriptions": [
        "Netflix",
        "Spotify",
        "Amazon Prime"
    ],

    "Other": [
        "Miscellaneous",
        "Other Expense"
    ]
}


# ============================================================
# CUSTOMER PROFILES
# ============================================================

profiles = {
    "High Saver": {
        "expense_ratio": (0.45, 0.60)
    },

    "Balanced": {
        "expense_ratio": (0.60, 0.75)
    },

    "Moderate Saver": {
        "expense_ratio": (0.75, 0.88)
    }
}


# ============================================================
# GENERATE CUSTOMERS
# ============================================================

users = []

for user_id in range(1, NUM_USERS + 1):

    monthly_income = np.random.randint(
        30000,
        150001
    )

    profile_name = np.random.choice(
        list(profiles.keys()),
        p=[0.25, 0.50, 0.25]
    )

    users.append({
        "customer_id": f"CUST{user_id:04d}",
        "monthly_income": monthly_income,
        "profile": profile_name
    })


users_df = pd.DataFrame(users)


# ============================================================
# GENERATE TRANSACTIONS
# ============================================================

transactions = []

transaction_id = 1

start_date = pd.Timestamp("2026-04-01")


for _, user in users_df.iterrows():

    customer_id = user["customer_id"]
    income = user["monthly_income"]
    profile_name = user["profile"]

    min_ratio, max_ratio = profiles[
        profile_name
    ]["expense_ratio"]


    # --------------------------------------------------------
    # Generate 6 months of data
    # --------------------------------------------------------

    for month in range(MONTHS):

        month_start = start_date + pd.DateOffset(
            months=month
        )

        # Slight income variation
        monthly_income = income * np.random.uniform(
            0.97,
            1.03
        )

        monthly_income = round(
            monthly_income,
            0
        )


        # ----------------------------------------------------
        # Salary
        # ----------------------------------------------------

        salary_date = month_start + pd.Timedelta(
            days=0
        )

        transactions.append({
            "transaction_id": transaction_id,
            "customer_id": customer_id,
            "transaction_date": salary_date,
            "transaction_type": "Income",
            "category": "Salary",
            "description": "Monthly Salary",
            "amount": monthly_income
        })

        transaction_id += 1


        # ----------------------------------------------------
        # Total monthly expense budget
        # ----------------------------------------------------

        expense_ratio = np.random.uniform(
            min_ratio,
            max_ratio
        )

        total_expense_budget = (
            monthly_income * expense_ratio
        )


        # ----------------------------------------------------
        # Category allocation
        # ----------------------------------------------------

        category_weights = {
            "Rent": 0.22,
            "Food": 0.13,
            "Transport": 0.08,
            "Utilities": 0.07,
            "Shopping": 0.09,
            "Entertainment": 0.05,
            "Healthcare": 0.04,
            "Insurance": 0.06,
            "Education": 0.05,
            "Subscriptions": 0.03,
            "Other": 0.08
        }


        # Normalize weights
        weight_sum = sum(
            category_weights.values()
        )

        for category in category_weights:

            category_weights[category] /= weight_sum


        # ----------------------------------------------------
        # Number of transactions
        # ----------------------------------------------------

        num_transactions = np.random.randint(
            30,
            61
        )


        # Randomly select categories
        selected_categories = np.random.choice(
            list(category_weights.keys()),
            size=num_transactions,
            p=list(category_weights.values())
        )


        # Initial random amounts
        raw_amounts = np.random.uniform(
            100,
            3000,
            size=num_transactions
        )


        # Scale total expenses to budget
        raw_amounts = (
            raw_amounts
            / raw_amounts.sum()
            * total_expense_budget
        )


        # ----------------------------------------------------
        # Create transactions
        # ----------------------------------------------------

        for category, amount in zip(
            selected_categories,
            raw_amounts
        ):

            transaction_date = (
                month_start
                + pd.Timedelta(
                    days=np.random.randint(0, 28)
                )
            )

            amount = round(
                max(amount, 50),
                2
            )

            description = np.random.choice(
                descriptions[category]
            )

            transactions.append({
                "transaction_id": transaction_id,
                "customer_id": customer_id,
                "transaction_date": transaction_date,
                "transaction_type": "Expense",
                "category": category,
                "description": description,
                "amount": amount
            })

            transaction_id += 1


# ============================================================
# CREATE DATAFRAME
# ============================================================

transactions_df = pd.DataFrame(
    transactions
)


# ============================================================
# SORT DATA
# ============================================================

transactions_df = transactions_df.sort_values(
    [
        "customer_id",
        "transaction_date"
    ]
)


# ============================================================
# SAVE
# ============================================================

transactions_df.to_csv(
    "data/transactions.csv",
    index=False
)


# ============================================================
# VALIDATION
# ============================================================

print(
    f"Generated {len(transactions_df):,} transactions."
)

print(
    f"Generated data for {NUM_USERS} customers."
)

print(
    f"Generated {MONTHS} months of financial history."
)

print(
    "Saved to data/transactions.csv"
)