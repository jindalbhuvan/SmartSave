import pandas as pd
import mysql.connector


# -----------------------------
# 1. Load CSV
# -----------------------------

csv_path = "data/transactions.csv"

df = pd.read_csv(csv_path)

print("CSV loaded successfully.")
print("Total transactions:", len(df))


# -----------------------------
# 2. Connect to MySQL
# -----------------------------

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="19oct2004",
    database="smartsave_db"
)

cursor = connection.cursor()

print("Connected to MySQL.")


# -----------------------------
# 3. Insert customers
# -----------------------------

customer_ids = df["customer_id"].unique()

customer_query = """
INSERT IGNORE INTO customers
(customer_id, name)
VALUES (%s, %s)
"""

for customer_id in customer_ids:

    name = f"Customer {customer_id}"

    cursor.execute(
        customer_query,
        (customer_id, name)
    )


print("Customers inserted:", len(customer_ids))


# -----------------------------
# 4. Insert transactions
# -----------------------------

transaction_query = """
INSERT INTO transactions
(
    customer_id,
    transaction_date,
    transaction_type,
    category,
    description,
    amount
)
VALUES (%s, %s, %s, %s, %s, %s)
"""

for _, row in df.iterrows():

    cursor.execute(
        transaction_query,
        (
            row["customer_id"],
            row["transaction_date"],
            row["transaction_type"],
            row["category"],
            row["description"],
            row["amount"]
        )
    )


# -----------------------------
# 5. Save changes
# -----------------------------

connection.commit()

print("Transactions inserted:", len(df))

cursor.close()
connection.close()

print("MySQL connection closed.")
print("Data migration completed successfully!")